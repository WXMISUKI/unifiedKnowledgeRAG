import re
from dataclasses import dataclass


PARSER_ID = "bracketed-citation-output-parser-v1"


@dataclass(frozen=True)
class ParsedAnswerOutput:
    answer_text: str
    citations: list[str]

    def metadata(self) -> dict[str, object]:
        return {
            "parser": PARSER_ID,
            "citation_count": len(self.citations),
        }


def parse_cited_answer_output(answer_text: str) -> ParsedAnswerOutput:
    citations: list[str] = []
    seen: set[str] = set()
    for citation in re.findall(r"\[([^\[\]]+)\]", answer_text):
        normalized = citation.strip()
        if not normalized or normalized in seen:
            continue
        seen.add(normalized)
        citations.append(normalized)
    return ParsedAnswerOutput(answer_text=answer_text, citations=citations)
