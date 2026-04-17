#!/usr/bin/env python3
"""Build a structured prompt for Poe external review from local files."""

from __future__ import annotations

import argparse
from pathlib import Path


TEMPLATE_HINTS = {
    "rebuttal-review": {
        "title": "Rebuttal Review Package",
        "ask": (
            "Judge whether the current rebuttal adequately addresses the reviewer. "
            "Be skeptical, concrete, and prefer minimal high-yield improvements."
        ),
    },
    "paper-claim-review": {
        "title": "Paper Claim Review Package",
        "ask": (
            "Judge whether the target claims are supported by the supplied evidence. "
            "Identify overclaim and propose the smallest safe rewrites."
        ),
    },
    "experiment-critique": {
        "title": "Experiment Critique Package",
        "ask": (
            "Judge whether the current experiment package is sufficient to support the claim. "
            "Recommend at most one small extra experiment if truly necessary."
        ),
    },
    "decision-cross-check": {
        "title": "Decision Cross-Check Package",
        "ask": (
            "Provide an independent second opinion on the proposed decision, wording, or plan. "
            "Focus on hidden risks and the best minimal correction."
        ),
    },
}

MODE_INSTRUCTIONS = {
    "rebuttal-review": {
        "rules": [
            "Be skeptical and concrete.",
            "Do not reward polite wording unless it truly answers the concern.",
            "Treat claim-evidence alignment as a hard constraint.",
            "If the rebuttal narrows a claim without truly resolving it by evidence, treat that as `部分解决`, not automatically `已解决`.",
            "Do not recommend broad new experiments unless they are genuinely high-value for rebuttal.",
            "If wording change is enough, say so directly.",
            "Focus on sentence-level rebuttal improvements, not a full rewrite.",
        ],
        "structure": [
            "## 1. Overall Judgment",
            "Use one of: `基本解决` / `部分解决` / `仍未解决`.",
            "## 2. Issue-by-Issue Assessment",
            "For each major concern, label it as `已解决` / `部分解决` / `未解决`, then explain briefly why.",
            "## 3. Remaining Risks",
            "Identify the top 1-3 issues most likely to keep the reviewer unconvinced.",
            "## 4. Best Minimal Improvements",
            "Prefer wording changes or clearer citation to existing evidence. Recommend at most one small experiment only if truly necessary.",
            "## 5. Direct Rebuttal Edits",
            "Rewrite the 1-3 most valuable rebuttal sentences in polished English, only if they should change.",
            "## 6. Five-Dimension Snapshot",
            "Briefly judge: contribution, writing clarity, experimental strength, evaluation completeness, and method design soundness.",
        ],
    },
    "paper-claim-review": {
        "rules": [
            "Be strict about evidence.",
            "Do not reward elegant writing if the claim overreaches.",
            "Treat claim-evidence alignment as a hard constraint.",
            "Evaluate whether the section has a clear `What / Why / So What` structure.",
            "Prefer the smallest safe rewrite over broad rewriting.",
        ],
        "structure": [
            "## 1. Overall Judgment",
            "Use one of: `表述稳健` / `略有过强` / `明显过强`.",
            "## 2. Claim-by-Claim Assessment",
            "For each major claim, state what is claimed, what evidence is provided, and whether it is supported.",
            "## 3. Most Dangerous Overclaims",
            "Identify the top 1-3 phrases or sentences most likely to trigger reviewer pushback.",
            "## 4. Best Minimal Rewrites",
            "Rewrite only the smallest number of sentences needed to make the section defensible.",
            "## 5. Narrative Check",
            "State whether the section clearly answers: What is claimed? Why is it supported? Why should the reader care?",
        ],
    },
    "experiment-critique": {
        "rules": [
            "Be concrete and economical.",
            "Do not ask for broad new experimental programs.",
            "Treat experiment-to-claim mapping as a hard constraint.",
            "If a wording fix or clearer citation to existing results is enough, say so.",
            "Recommend at most one small extra experiment only if it has unusually high value.",
        ],
        "structure": [
            "## 1. Overall Assessment",
            "Use one of: `证据基本够用` / `证据较强但仍有缺口` / `证据仍不足`.",
            "## 2. What Already Works",
            "List the parts already supported by current evidence.",
            "## 3. Remaining Vulnerabilities",
            "List the top 1-3 weaknesses most likely to be attacked by a reviewer.",
            "## 4. Best Next Move",
            "For each vulnerability, choose: `只改措辞` / `更清楚引用已有结果` / `新增一个小实验` / `不值得继续投入`.",
            "## 5. If One Extra Experiment Is Worth Doing",
            "State exactly which single experiment would provide the highest value.",
            "## 6. Claim-Evidence Check",
            "For the main experimental claim, summarize `Claim`, `Evidence`, and `Status: supported / partially supported / unsupported`.",
        ],
    },
    "decision-cross-check": {
        "rules": [
            "Act as an independent second opinion, not a coauthor.",
            "Focus on hidden risks, weak assumptions, and avoidable overcommitment.",
            "Prefer the smallest correction that materially improves the decision or wording.",
        ],
        "structure": [
            "## 1. Overall Judgment",
            "State whether the current decision or wording is `稳妥` / `可行但有风险` / `不够稳妥`.",
            "## 2. Main Risks",
            "List the top 1-3 hidden risks or weak assumptions.",
            "## 3. Best Minimal Fix",
            "State the best minimal correction.",
            "## 4. Direct Rewrite or Recommendation",
            "Provide a direct rewrite or a concrete revised decision if needed.",
        ],
    },
}

PRESET_FOCUS = {
    "concept-validity": (
        "Focus especially on concept extraction versus concept learning, "
        "agreement versus correctness, shared-bias explanations, whether the "
        "semantic layer is truly validated, and whether claims are now properly narrowed."
    ),
    "runtime-scope": (
        "Focus especially on runtime and deployment practicality, protocol clarity, "
        "dataset or benchmark scope, positioning breadth, and whether the reply feels complete and credible."
    ),
    "silver-labels": (
        "Focus especially on silver versus gold labels, weak-supervision limitations, "
        "whether proxy annotations are being overclaimed, and whether known weak signals are honestly handled."
    ),
    "hardline-methodology": (
        "Focus especially on whether requested controls are truly provided, whether proxies are being passed off as direct answers, "
        "fairness of comparisons, robustness-scope overreach, and whether the contribution reads as methodologically solid."
    ),
    "claim-tightening": (
        "Focus especially on overclaim, weak claim-evidence mapping, ambiguous qualifiers, "
        "and the smallest sentence-level changes needed to make the text defensible."
    ),
}


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--mode",
        required=True,
        choices=sorted(TEMPLATE_HINTS),
        help="Review mode.",
    )
    parser.add_argument("--paper-excerpts", help="Markdown file with relevant paper excerpts.")
    parser.add_argument("--reviewer-comments", help="Markdown file with reviewer comments.")
    parser.add_argument("--current-reply", help="Markdown file with current rebuttal or target text.")
    parser.add_argument("--evidence-notes", help="Markdown file with experiment notes or supporting evidence.")
    parser.add_argument(
        "--preset",
        choices=sorted(PRESET_FOCUS),
        help="Optional reusable reviewer-style preset.",
    )
    parser.add_argument("--focus", help="Short reviewer-specific or task-specific focus block.")
    parser.add_argument("--language", default="Chinese", help="Requested output language.")
    parser.add_argument("--output-file", help="Optional output file path. Defaults to stdout.")
    return parser.parse_args()


def read_optional(path: str | None) -> str | None:
    if not path:
        return None
    return Path(path).read_text(encoding="utf-8").strip()


def build_prompt(
    *,
    mode: str,
    language: str,
    paper_excerpts: str | None = None,
    reviewer_comments: str | None = None,
    current_reply: str | None = None,
    evidence_notes: str | None = None,
    preset: str | None = None,
    focus: str | None = None,
) -> str:
    sections: list[str] = []
    hint = TEMPLATE_HINTS[mode]

    sections.append(f"# {hint['title']}")
    sections.append("You are acting as a skeptical external reviewer.")
    sections.append(f"Main task: {hint['ask']}")
    sections.append(f"Please answer in {language}.")

    focus_parts: list[str] = []
    if preset:
        focus_parts.append(PRESET_FOCUS[preset])
    if focus:
        focus_parts.append(focus.strip())

    if focus_parts:
        sections.append("## Focus")
        sections.append("\n".join(f"- {part}" for part in focus_parts))

    mode_info = MODE_INSTRUCTIONS[mode]
    sections.append("## Important Rules")
    sections.append("\n".join(f"- {rule}" for rule in mode_info["rules"]))
    sections.append("## Required Output Format")
    sections.append(
        "Use the exact markdown section headings below so the result can be summarized reliably."
    )
    sections.append("\n".join(f"- {line}" for line in mode_info["structure"]))

    def add_section(title: str, content: str | None) -> None:
        if content:
            sections.append(f"## {title}")
            sections.append(content)

    add_section("Paper Excerpts", paper_excerpts)
    add_section("Reviewer Comments", reviewer_comments)
    add_section("Current Reply or Target Text", current_reply)
    add_section("Evidence Notes", evidence_notes)

    return "\n\n".join(sections).strip() + "\n"


def main() -> int:
    args = parse_args()
    prompt = build_prompt(
        mode=args.mode,
        language=args.language,
        paper_excerpts=read_optional(args.paper_excerpts),
        reviewer_comments=read_optional(args.reviewer_comments),
        current_reply=read_optional(args.current_reply),
        evidence_notes=read_optional(args.evidence_notes),
        preset=args.preset,
        focus=args.focus,
    )

    if args.output_file:
        Path(args.output_file).write_text(prompt, encoding="utf-8")
    else:
        print(prompt)

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
