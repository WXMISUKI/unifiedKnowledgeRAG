from app.services.answer_output_parser import parse_cited_answer_output


def test_output_parser_extracts_unique_citations_in_order():
    parsed = parse_cited_answer_output(
        "[a#1] 第一条。\n[b#2] 第二条。\n[a#1] 重复引用。"
    )

    assert parsed.answer_text == "[a#1] 第一条。\n[b#2] 第二条。\n[a#1] 重复引用。"
    assert parsed.citations == ["a#1", "b#2"]
    assert parsed.metadata() == {
        "parser": "bracketed-citation-output-parser-v1",
        "citation_count": 2,
    }


def test_output_parser_reports_missing_citations():
    parsed = parse_cited_answer_output("这是一条没有引用的回答。")

    assert parsed.citations == []
    assert parsed.metadata() == {
        "parser": "bracketed-citation-output-parser-v1",
        "citation_count": 0,
    }
