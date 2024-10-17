from dataclasses import dataclass

MSG_SEPARATOR = b"\r\n"

@dataclass
class SimpleString:
    data: str

def extract_frame_from_buffer(buffer):
    match chr(buffer[0]):
        case '+':
            seperator = buffer.find(MSG_SEPARATOR)

            if seperator != -1:
                return SimpleString(buffer[1:seperator].decode()), seperator + 2
    return None, 0

def test_read_frame_simple_string_incomplete_frame():
    buffer = b"+Par"
    frame, frame_size = extract_frame_from_buffer(buffer)
    assert frame == None
    assert frame_size == 0


def test_read_frame_simple_string_complete_frame():
    buffer = b"+OK\r\n"
    frame, frame_size = extract_frame_from_buffer(buffer)
    assert frame == SimpleString("OK")
    assert frame_size == 5


def test_read_frame_simple_string_extra_data():
    buffer = b"+OK\r\n+Next"
    frame, frame_size = extract_frame_from_buffer(buffer)
    assert frame == SimpleString("OK")
    assert frame_size == 5
