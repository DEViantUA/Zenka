from typing import Dict, Tuple, Union, Optional


async def get_color_user(color: Dict[Union[int, str], Tuple[int, int, int]]) -> Optional[Dict[Union[int, str], Tuple[int, int, int]]]:
    processed_dict = {
        key: value
        for key, value in color.items()
        if isinstance(value, tuple) and 3 <= len(value) <= 4 and all(0 <= x <= 255 for x in value)
    }
    return processed_dict or {}
