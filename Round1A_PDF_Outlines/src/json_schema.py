SCHEMA = {
  "type": "object",
  "properties": {
    "title": {"type": "string"},
    "outline": {
      "type": "array",
      "items": {
        "type": "object",
        "properties": {
          "level": {"type": "string", "enum": ["H1", "H2", "H3"]},
          "text": {"type": "string"},
          "page": {"type": "integer", "minimum": 1}
        },
        "required": ["level", "text", "page"],
        "additionalProperties": False
      }
    }
  },
  "required": ["title", "outline"],
  "additionalProperties": False
}
