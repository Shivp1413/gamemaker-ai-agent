import streamlit as st

def clean_message(message):
    """Clean and format the message for display"""
    lines = message.split('\n')
    cleaned_lines = []
    in_code_block = False
    
    for line in lines:
        if line.strip().startswith('```'):
            in_code_block = not in_code_block
            if 'python' in line:
                cleaned_lines.append('```python')
            else:
                cleaned_lines.append('```')
        else:
            cleaned_lines.append(line)
    
    return '\n'.join(cleaned_lines)

def extract_version_content(message):
    """Extract content from a version submission"""
    try:
        if "===VERSION_START===" not in message or "===VERSION_END===" not in message:
            return None

        content = message.split("===VERSION_START===")[1].split("===VERSION_END===")[0].strip()
        
        description = ""
        code = ""
        instructions = ""
        
        if "DESCRIPTION:" in content:
            description = content.split("DESCRIPTION:")[1].split("CODE:")[0].strip()
        
        if "CODE:" in content:
            code_section = content.split("CODE:")[1].split("INSTRUCTIONS:")[0].strip()
            code = code_section.replace("```python", "").replace("```", "").strip()
        
        if "INSTRUCTIONS:" in content:
            instructions = content.split("INSTRUCTIONS:")[1].strip()

        return {
            "description": description,
            "code": code,
            "instructions": instructions
        }
    except Exception as e:
        print(f"Error extracting version content: {str(e)}")
        return None

def format_message_for_display(message):
    """Format message for display in Streamlit"""
    if "```" in message:
        parts = message.split("```")
        formatted_parts = []
        for i, part in enumerate(parts):
            if i % 2 == 0:  # Text part
                formatted_parts.append(part)
            else:  # Code part
                lang = "python" if part.startswith("python\n") else ""
                code = part[len(lang):] if lang else part
                formatted_parts.append(f'<div class="code-block">{st.code(code, language=lang)}</div>')
        return "".join(formatted_parts)
    return message