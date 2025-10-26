#!/usr/bin/env python3
"""
PASSWORD PROFILER - Advanced Password Generation Tool
Developed by R00tghost
"""

import random
import string
import sys
from datetime import datetime

class PasswordProfiler:
    def __init__(self):
        self.banner()
        
    def banner(self):
        print(r"""
        ____                         ____                ____ _  __           
       / __ \ ____ _ _____ _____    / __ \ _____ ____   / __/(_)/ /___   _____
      / /_/ // __ `// ___// ___/   / /_/ // ___// __ \ / /_ / // // _ \ / ___/
     / ____// /_/ /(__  )(__  )_  / ____// /   / /_/ // __// // //  __// /    
    /_/     \__,_//____//____/(_)/_/    /_/    \____//_/  /_//_/ \___//_/     
                                                                          
                    Developed by: R00tGh0st
        """)

    def get_user_input(self, prompt, validation_type='text'):
        """Get and validate user input"""
        while True:
            try:
                user_input = input(prompt).strip()
                
                if validation_type == 'y/n':
                    if user_input.lower() in ['y', 'yes', 'n', 'no']:
                        return user_input.lower() in ['y', 'yes']
                    else:
                        print("Please enter 'y' or 'n'")
                elif validation_type == 'number':
                    if user_input.isdigit():
                        return int(user_input)
                    else:
                        print("Please enter a valid number")
                elif validation_type == 'date':
                    if user_input and self.validate_date(user_input):
                        return user_input
                    elif not user_input:
                        return ""
                    else:
                        print("Please enter date in DD/MM/YYYY format")
                elif validation_type == 'phone':
                    if user_input and self.validate_phone(user_input):
                        return user_input
                    elif not user_input:
                        return ""
                    else:
                        print("Please enter phone number without country code (10 digits)")
                else:
                    return user_input
            except KeyboardInterrupt:
                print("\n\nOperation cancelled by user!")
                sys.exit(0)

    def validate_date(self, date_str):
        """Validate date format DD/MM/YYYY"""
        try:
            # Check if date contains slashes
            if '/' not in date_str:
                return False
                
            parts = date_str.split('/')
            if len(parts) != 3:
                return False
                
            day, month, year = parts
            
            if len(day) != 2 or len(month) != 2 or len(year) != 4:
                return False
                
            if not day.isdigit() or not month.isdigit() or not year.isdigit():
                return False
                
            day_int = int(day)
            month_int = int(month)
            year_int = int(year)
            
            # Basic date validation
            if month_int < 1 or month_int > 12:
                return False
            if day_int < 1 or day_int > 31:
                return False
            if year_int < 1900 or year_int > datetime.now().year:
                return False
                
            return True
        except:
            return False

    def validate_phone(self, phone_str):
        """Validate phone number (10 digits without country code)"""
        # Remove any spaces, dashes, etc.
        clean_phone = ''.join(filter(str.isdigit, phone_str))
        return len(clean_phone) == 10 and clean_phone.isdigit()

    def extract_date_parts(self, date_str):
        """Extract different parts from date in DD/MM/YYYY format"""
        if not date_str:
            return []
            
        parts = date_str.split('/')
        if len(parts) != 3:
            return []
            
        day, month, year = parts
        year_short = year[2:]
        
        # Return various date combinations
        return [day, month, year, year_short, day + month, month + year, day + month + year_short]

    def clean_phone_number(self, phone_str):
        """Clean and extract phone number parts"""
        if not phone_str:
            return []
            
        # Remove non-digit characters
        clean_phone = ''.join(filter(str.isdigit, phone_str))
        
        if len(clean_phone) == 10:
            return [
                clean_phone,  # Full number
                clean_phone[-4:],  # Last 4 digits
                clean_phone[:3],  # First 3 digits
                clean_phone[3:6],  # Middle 3 digits
                clean_phone[-6:],  # Last 6 digits
            ]
        return []

    def get_personal_info(self):
        """Collect personal information for password profiling"""
        print("\n" + "="*60)
        print("PERSONAL INFORMATION COLLECTION")
        print("="*60)
        
        personal_data = {}
        
        # Full Name
        full_name = self.get_user_input("Full name: ")
        personal_data['full_name'] = full_name.lower()
        
        # Date of Birth
        dob_required = self.get_user_input("dob y/n: ", 'y/n')
        if dob_required:
            dob = self.get_user_input("please enter dob (DD/MM/YYYY): ", 'date')
            personal_data['dob'] = self.extract_date_parts(dob)
        else:
            personal_data['dob'] = []
        
        # Father's Information
        print("\n--- Father's Information ---")
        father_name = self.get_user_input("father: ")
        personal_data['father'] = father_name.lower()
        
        father_dob_required = self.get_user_input("dob y/n: ", 'y/n')
        if father_dob_required:
            father_dob = self.get_user_input("please enter dob (DD/MM/YYYY): ", 'date')
            personal_data['father_dob'] = self.extract_date_parts(father_dob)
        else:
            personal_data['father_dob'] = []
        
        # Mother's Information
        print("\n--- Mother's Information ---")
        mother_name = self.get_user_input("mother: ")
        personal_data['mother'] = mother_name.lower()
        
        mother_dob_required = self.get_user_input("dob y/n: ", 'y/n')
        if mother_dob_required:
            mother_dob = self.get_user_input("please enter dob (DD/MM/YYYY): ", 'date')
            personal_data['mother_dob'] = self.extract_date_parts(mother_dob)
        else:
            personal_data['mother_dob'] = []
        
        # Phone Number
        print("\n--- Contact Information ---")
        phone_required = self.get_user_input("ph y/n: ", 'y/n')
        if phone_required:
            phone = self.get_user_input("enter ph (without +91): ", 'phone')
            personal_data['phone'] = self.clean_phone_number(phone)
        else:
            personal_data['phone'] = []
        
        return personal_data

    def generate_password_variations(self, base_words, numbers, special_chars=False):
        """Generate password variations from base words and numbers (8-10 chars only)"""
        variations = set()
        
        # Common substitutions
        substitutions = {
            'a': ['@', '4'],
            'e': ['3'],
            'i': ['1', '!'],
            'o': ['0'],
            's': ['5', '$'],
            't': ['7'],
            'l': ['1'],
            'b': ['8', '6']
        }
        
        # Combine all base elements
        all_elements = base_words + numbers
        
        # Generate combinations with length restriction
        for i in range(len(all_elements)):
            for j in range(len(all_elements)):
                if i != j:
                    # Basic combinations
                    combos = [
                        all_elements[i] + all_elements[j],
                        all_elements[i] + "_" + all_elements[j],
                        all_elements[i] + "." + all_elements[j],
                        all_elements[i] + "-" + all_elements[j],
                        all_elements[i].capitalize() + all_elements[j],
                        all_elements[i] + all_elements[j].capitalize(),
                        all_elements[i].capitalize() + all_elements[j].capitalize(),
                        all_elements[j] + all_elements[i],
                        all_elements[j].capitalize() + all_elements[i]
                    ]
                    
                    # Filter combinations by length (8-10 characters)
                    for combo in combos:
                        if 8 <= len(combo) <= 10:
                            variations.add(combo)
        
        # Add single elements with common suffixes (length restricted)
        common_suffixes = ['123', '1234', '1', '12', '!', '@', '#', '007', '100', '99', '88']
        for element in all_elements:
            for suffix in common_suffixes:
                combo1 = element + suffix
                combo2 = element.capitalize() + suffix
                
                if 8 <= len(combo1) <= 10:
                    variations.add(combo1)
                if 8 <= len(combo2) <= 10:
                    variations.add(combo2)
        
        # Add special character variations if requested (with length restriction)
        if special_chars:
            special_variations = set()
            special_prefixes = ['!', '@', '#', '$']
            special_suffixes = ['!', '@', '#', '$']
            
            # Add special characters to existing variations
            for var in list(variations):
                for prefix in special_prefixes:
                    new_var = prefix + var
                    if 8 <= len(new_var) <= 10:
                        special_variations.add(new_var)
                
                for suffix in special_suffixes:
                    new_var = var + suffix
                    if 8 <= len(new_var) <= 10:
                        special_variations.add(new_var)
            
            # Apply character substitutions with length check
            for var in list(variations):
                for char, replacements in substitutions.items():
                    if char in var.lower():
                        for replacement in replacements:
                            modified = var.replace(char, replacement)
                            if 8 <= len(modified) <= 10:
                                special_variations.add(modified)
                            
                            # Also try capitalized version
                            modified_cap = var.replace(char.capitalize(), replacement)
                            if modified_cap != var and 8 <= len(modified_cap) <= 10:
                                special_variations.add(modified_cap)
            
            variations.update(special_variations)
        
        # Final length validation
        valid_variations = [pwd for pwd in variations if 8 <= len(pwd) <= 10]
        return valid_variations

    def generate_passwords(self, personal_data, count, special_chars):
        """Generate passwords based on personal data (8-10 chars only)"""
        print(f"\nGenerating {count} passwords (8-10 characters)...")
        
        # Prepare base words and numbers
        base_words = []
        numbers = []
        
        # Add names and split into parts
        if personal_data['full_name']:
            base_words.append(personal_data['full_name'])
            name_parts = personal_data['full_name'].split()
            base_words.extend(name_parts)
            # Add initials (only if they help create valid lengths)
            if len(name_parts) > 1:
                initials = ''.join([part[0] for part in name_parts])
                if 2 <= len(initials) <= 6:  # Reasonable length for combinations
                    base_words.append(initials)
                    base_words.append(initials.lower())
        
        if personal_data['father']:
            base_words.append(personal_data['father'])
            father_parts = personal_data['father'].split()
            base_words.extend(father_parts)
        
        if personal_data['mother']:
            base_words.append(personal_data['mother'])
            mother_parts = personal_data['mother'].split()
            base_words.extend(mother_parts)
        
        # Add date parts
        numbers.extend(personal_data['dob'])
        numbers.extend(personal_data['father_dob'])
        numbers.extend(personal_data['mother_dob'])
        
        # Add phone number parts
        numbers.extend(personal_data['phone'])
        
        # Remove duplicates and empty strings, and filter elements that are too long
        base_words = list(set([w for w in base_words if w and len(w) <= 8]))
        numbers = list(set([n for n in numbers if n and len(n) <= 8]))
        
        print(f"Base words: {len(base_words)}, Numbers: {len(numbers)}")
        
        # Generate password variations
        passwords = self.generate_password_variations(base_words, numbers, special_chars)
        
        # If we need more passwords, add some random combinations (8-10 chars)
        if len(passwords) < count:
            additional_needed = count - len(passwords)
            print(f"Generating {additional_needed} additional random passwords (8-10 chars)...")
            passwords.extend(self.generate_random_passwords(additional_needed, special_chars))
        
        # Ensure we have exactly the requested number and shuffle
        random.shuffle(passwords)
        final_passwords = passwords[:count]
        
        # Final validation - ensure all passwords are 8-10 characters
        validated_passwords = [pwd for pwd in final_passwords if 8 <= len(pwd) <= 10]
        
        if len(validated_passwords) < count:
            print(f"Warning: Only generated {len(validated_passwords)} valid passwords (8-10 chars)")
        
        return validated_passwords

    def generate_random_passwords(self, count, special_chars):
        """Generate additional random passwords (8-10 characters only)"""
        random_passwords = []
        characters = string.ascii_letters + string.digits
        if special_chars:
            characters += "!@#$%&*"
        
        for _ in range(count):
            length = random.randint(8, 10)  # Only 8, 9, or 10 characters
            password = ''.join(random.choice(characters) for _ in range(length))
            random_passwords.append(password)
        
        return random_passwords

    def save_to_file(self, passwords, filename):
        """Save passwords to file - clean format without headers"""
        try:
            with open(filename, 'w', encoding='utf-8') as f:
                # Write only the passwords, one per line
                for password in passwords:
                    f.write(password + '\n')
            
            print(f"✓ Passwords saved to: {filename}")
            print(f"✓ Total passwords generated: {len(passwords)}")
            print(f"✓ Password length: 8-10 characters")
        except Exception as e:
            print(f"✗ Error saving to file: {e}")

    def run(self):
        """Main function to run the password profiler"""
        try:
            # Get personal information
            personal_data = self.get_personal_info()
            
            # Get generation parameters
            print("\n" + "="*60)
            print("PASSWORD GENERATION SETTINGS")
            print("="*60)
            
            count = self.get_user_input("No of count: ", 'number')
            special_chars = self.get_user_input("add special characters : y/n: ", 'y/n')
            
            # Generate passwords
            passwords = self.generate_passwords(personal_data, count, special_chars)
            
            # Save to file
            save_file = self.get_user_input("file name y/n: ", 'y/n')
            if save_file:
                filename = self.get_user_input("enter file name: ")
                if not filename.endswith('.txt'):
                    filename += '.txt'
            else:
                # Default filename
                filename = "target.txt"
                print(f"Using default filename: {filename}")
            
            self.save_to_file(passwords, filename)
            
            # Display sample of passwords with lengths
            print("\n" + "="*60)
            print("SAMPLE OF GENERATED PASSWORDS (first 10)")
            print("="*60)
            for i, password in enumerate(passwords[:10], 1):
                print(f"{password} (length: {len(password)})")
            
            remaining = len(passwords) - 10
            if remaining > 0:
                print(f"\n... and {remaining} more passwords in {filename}")
            else:
                print(f"\nAll {len(passwords)} passwords shown above")
                
            print("\n" + "="*60)
            print("PASSWORD PROFILING COMPLETED!")
            print("="*60)
            
        except KeyboardInterrupt:
            print("\n\nOperation cancelled by user!")
        except Exception as e:
            print(f"\nAn error occurred: {e}")

if __name__ == "__main__":
    profiler = PasswordProfiler()
    profiler.run()
