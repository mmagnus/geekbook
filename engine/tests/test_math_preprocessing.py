from engine.preprocessing import convert_tex_math_delimiters


def test_convert_display_math_from_double_dollars():
    text = r"$$\text{zasięg} = \frac{72}{11} \times 100 \approx 655 \text{ km}$$"

    converted = convert_tex_math_delimiters(text)

    assert (
        converted ==
        r'<script type="math/tex; mode=display">\text{zasięg} = \frac{72}{11} \times 100 \approx 655 \text{ km}</script>'
    )


def test_convert_parenthesized_and_bracketed_tex():
    text = r"Inline \(x + y\) and block \[x^2\]"

    converted = convert_tex_math_delimiters(text)

    assert r'<script type="math/tex">x + y</script>' in converted
    assert r'<script type="math/tex; mode=display">x^2</script>' in converted


def test_leave_fenced_code_and_existing_script_tags_unchanged():
    text = (
        "```tex\n$$x$$\n```\n\n"
        '<script type="math/tex">e^x</script>'
    )

    converted = convert_tex_math_delimiters(text)

    assert "```tex\n$$x$$\n```" in converted
    assert '<script type="math/tex">e^x</script>' in converted
