import re

def extract_hour(text):
    """Extracts the entry and exit times from a string"""
 
    pattern = r'(\d{1,2}h(?:\d{2})?)\s*(?:às?|à)\s*(\d{1,2}h(?:\d{2})?)|\b(\d{1,2}:\d{2}(:\d{2})?)\s*(?:às?|à)\s*(\d{1,2}:\d{2}(:\d{2})?)\b|(\d{1,2}:\d{2})\s*–\s*(\d{1,2}:\d{2})'
    
    # (\d{1,2}h(?:\d{2})?)\s*(?:às?|à)\s*          Group 1: 17h or 17h30
    # (\d{1,2}h(?:\d{2})?)                         Group 2: 00h or 00h30
    # \b(\d{1,2}:\d{2}(:\d{2})?)\s*(?:às?|à)\s*    Group 3: 17:00 or 17:00:00
    # (\d{1,2}:\d{2}(:\d{2})?)\b                   Group 4: 00:30 ou 00:30:00
    # (\d{1,2}:\d{2})\s*–\s*(\d{1,2}:\d{2})        Group 5 and 6: 11:00 – 01:00
    
    text = text.strip()

    match = re.search(pattern, text)
    
    if match:
        # HHh or HHhMM
        if match.group(1) and match.group(2):
            entry_time = time_format(match.group(1))
            exit_time = time_format(match.group(2))
        # HH:MM or HH:MM:SS
        elif match.group(3) and match.group(4):
            entry_time = time_format(match.group(3))
            exit_time = time_format(match.group(5))
        # Separetor = "–"
        elif match.group(7) and match.group(8):
            entry_time = time_format(match.group(7))
            exit_time = time_format(match.group(8))
        else:
            return None, None
        
        return entry_time, exit_time
    else:
        return None, None


def time_format(time_str):
    """Format time in HH:MM"""
    
    # Remove seconds 17:00:00 → 17:00
    if ':' in time_str and len(time_str.split(':')) == 3:
        time_str = ':'.join(time_str.split(':')[:2])
    
    if 'h' in time_str:
        if time_str[-1] == 'h':
            time_str = time_str.replace('h', ':00') 
        else:
            if len(time_str) <= 4:
                time_str = '0' + time_str.replace('h', ':') 
            else:
                time_str = time_str.replace('h', ':')

    # Transform 0h in 00
    if time_str.startswith('0') and len(time_str) == 4:
        time_str = '00' + time_str[1:]

    if not time_str.startswith('0') and len(time_str) == 4:
        time_str = '0' + time_str

    if len(time_str.split(':')) == 2:
        return time_str
    else:
        return time_str[:5]  