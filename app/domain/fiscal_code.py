_ODD_VALUES = {
    **dict(zip("0123456789", (1, 0, 5, 7, 9, 13, 15, 17, 19, 21), strict=True)),
    **dict(
        zip(
            "ABCDEFGHIJKLMNOPQRSTUVWXYZ",
            (1, 0, 5, 7, 9, 13, 15, 17, 19, 21, 2, 4, 18, 20, 11, 3, 6, 8, 12, 14, 16, 10, 22, 25, 24, 23),
            strict=True,
        )
    ),
}
_EVEN_VALUES = {
    **{str(value): value for value in range(10)},
    **{chr(ord("A") + value): value for value in range(26)},
}


def is_valid_fiscal_code(value: str) -> bool:
    code = value.strip().upper()
    if len(code) != 16 or not code.isalnum():
        return False

    total = sum(
        (_ODD_VALUES if position % 2 else _EVEN_VALUES)[character]
        for position, character in enumerate(code[:15], start=1)
    )
    return code[-1] == chr(ord("A") + total % 26)
