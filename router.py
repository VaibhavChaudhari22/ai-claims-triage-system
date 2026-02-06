
import re
from typing import Tuple, List, Dict, Any

def route_claim(data: dict) -> Tuple[List[str], str, str]:
    """Route claim based on extracted data"""
    
    # SIMPLE, RELIABLE APPROACH
    missing_fields = []
    
    # Only check if fields are truly empty or obviously placeholders
    required_fields = ["Policy Number", "Policyholder Name", "Date", 
                      "Description", "Estimated Damage", "Location"]
    
    for field in required_fields:
        value = data.get(field, "")
        
        # Check if empty
        if not value:
            missing_fields.append(field)
            continue
            
        # Special handling for Policyholder Name
        if field == "Policyholder Name":
            # If it contains actual name words (not field labels), it's valid
            if is_valid_name(value):
                continue
            else:
                missing_fields.append(field)
        else:
            # For other fields, just check if it's obviously a placeholder
            if is_obvious_placeholder(value):
                missing_fields.append(field)
    
    # Get values for routing
    description = data.get("Description", "").lower()
    estimate = parse_damage(data.get("Estimated Damage", "0"))
    claim_type = data.get("Claim Type", "").lower()
    
    # ROUTING LOGIC
    if missing_fields:
        route = "Manual Review"
        reason = f"Missing: {', '.join(missing_fields)}"
    
    elif has_fraud_indicators(description):
        route = "Investigation Flag"
        reason = "Potential fraud indicators"
    
    elif has_injury_indicators(description, claim_type):
        route = "Specialist Queue"
        reason = "Injury/medical related"
    
    elif estimate >= 1000000:
        route = "Executive Review"
        reason = f"Very high value: ${estimate:,.2f}"
    
    elif estimate >= 100000:
        route = "High Value Review"
        reason = f"High damage: ${estimate:,.2f}"
    
    elif estimate < 5000:
        route = "Fast-track"
        reason = f"Low damage: ${estimate:,.2f}"
    
    elif estimate < 25000:
        route = "Standard Review"
        reason = f"Moderate damage: ${estimate:,.2f}"
    
    else:
        route = "Extended Review"
        reason = f"Significant damage: ${estimate:,.2f}"
    
    return missing_fields, route, reason

def is_valid_name(text: str) -> bool:
    """Check if text is a valid name (not a field label)"""
    if not text or not isinstance(text, str):
        return False
    
    text = text.strip()
    
    # KNOWN FIELD LABELS (exact matches)
    field_labels = {
        "NAME OF INSURED",
        "NAME OF INSURED (FIRST, MIDDLE, LAST)",
        "NAME OF CONTACT (FIRST, MIDDLE, LAST)",
        "CONTACT NAME",
        "CONTACT NAME:"
    }
    
    if text.upper() in field_labels:
        return False
    
    # Check length - names should be reasonable length
    if len(text) < 2 or len(text) > 100:
        return False
    
    # Names should have letters
    if not any(c.isalpha() for c in text):
        return False
    
    # Check for common name patterns
    # Names usually have letters, spaces, commas, periods, apostrophes
    valid_chars = set("abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ ,.-'&")
    if all(c in valid_chars for c in text):
        # Has at least one letter and reasonable structure
        words = text.split()
        if len(words) >= 1:
            # Check each word has letters
            for word in words:
                if any(c.isalpha() for c in word):
                    return True
    
    return False

def is_obvious_placeholder(text: Any) -> bool:
    """Check if text is obviously a placeholder (not real data)"""
    if not isinstance(text, str):
        return True
    
    text = text.strip()
    
    # Empty
    if not text:
        return True
    
    # Common placeholders
    common_placeholders = {
        "", "N/A", "NA", "None", "Null", "TBD", "To be determined",
        "Enter text here", "Click to enter", "Select...", "Choose...",
        "Type here", "Please enter", "Not applicable", "Unknown"
    }
    
    if text in common_placeholders:
        return True
    
    # Field labels from ACORD forms
    acord_labels = [
        "NAME OF INSURED",
        "POLICY NUMBER", 
        "LOCATION OF LOSS",
        "DESCRIPTION OF ACCIDENT",
        "ESTIMATE AMOUNT",
        "E-MAIL ADDRESS",
        "PHONE #",
        "VEH #",
        "V.I.N.",
        "MAKE:",
        "MODEL:",
        "BODY TYPE",
        "PLATE NUMBER",
        "DATE OF LOSS",
        "AGENCY CUSTOMER ID",
        "CONTACT NAME:"
    ]
    
    text_upper = text.upper()
    for label in acord_labels:
        if text_upper == label:
            return True
    
    # Pattern: All caps with special chars and multiple words
    # But "QUICK DELIVERY SERVICES LLC" is a valid business name!
    # So we need to be more careful
    
    # Check if it's instructional text
    instructional_words = ["ENTER", "SELECT", "CHOOSE", "CLICK", "TYPE", "PLEASE"]
    for word in instructional_words:
        if word in text_upper and len(text) > 8:
            return True
    
    # Check for brackets/parentheses with placeholder text
    if re.search(r'\[.*\]|\(.*\)', text):
        placeholder_words = ["EXAMPLE", "E.G.", "I.E.", "SUCH AS"]
        for word in placeholder_words:
            if word in text_upper:
                return True
    
    return False

def parse_damage(value: Any) -> float:
    """Parse damage estimate from various formats"""
    try:
        if isinstance(value, (int, float)):
            return float(value)
        
        if isinstance(value, str):
            # Clean the string
            cleaned = re.sub(r'[^\d.]', '', value)
            if cleaned:
                return float(cleaned)
    except:
        pass
    
    return 0.0

def has_fraud_indicators(description: str) -> bool:
    """Check for fraud indicators"""
    fraud_keywords = ['fraud', 'staged', 'inconsistent', 'suspicious', 'fake']
    return any(keyword in description for keyword in fraud_keywords)

def has_injury_indicators(description: str, claim_type: str) -> bool:
    """Check for injury indicators"""
    injury_keywords = ['injury', 'medical', 'hospital', 'doctor', 'pain', 
                      'whiplash', 'treatment', 'ambulance', 'er ', 'x-ray']
    
    if any(keyword in claim_type for keyword in ['injury', 'medical']):
        return True
    
    return any(keyword in description for keyword in injury_keywords)