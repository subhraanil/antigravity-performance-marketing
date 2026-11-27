import pandas as pd
import json
import os

# Indian Pincode 3-Digit & 2-Digit Dictionary
PINCODE_LOOKUP = {
    # Delhi & NCR
    '110': ('Delhi', 'Delhi (NCR)', 'Delhi'),
    '121': ('Faridabad', 'Faridabad (NCR)', 'Haryana'),
    '122': ('Gurugram', 'Gurugram (NCR)', 'Haryana'),
    '123': ('Rewari', 'Haryana', 'Haryana'),
    '124': ('Rohtak', 'Haryana', 'Haryana'),
    '125': ('Hisar', 'Haryana', 'Haryana'),
    '131': ('Sonipat', 'Sonipat (NCR)', 'Haryana'),
    '132': ('Karnal', 'Haryana', 'Haryana'),
    '133': ('Ambala', 'Haryana', 'Haryana'),
    '134': ('Panchkula', 'Panchkula / Chandigarh', 'Haryana'),
    '141': ('Ludhiana', 'Ludhiana', 'Punjab'),
    '143': ('Amritsar', 'Amritsar', 'Punjab'),
    '144': ('Jalandhar', 'Jalandhar', 'Punjab'),
    '147': ('Patiala', 'Patiala', 'Punjab'),
    '151': ('Bathinda', 'Bathinda', 'Punjab'),
    '160': ('Chandigarh', 'Chandigarh', 'Chandigarh'),
    '171': ('Shimla', 'Shimla', 'Himachal Pradesh'),
    '180': ('Jammu', 'Jammu', 'Jammu & Kashmir'),
    '190': ('Srinagar', 'Srinagar', 'Jammu & Kashmir'),
    '201': ('Gautam Buddha Nagar / Ghaziabad', 'Noida / Ghaziabad (NCR)', 'Uttar Pradesh'),
    '202': ('Aligarh', 'Aligarh', 'Uttar Pradesh'),
    '203': ('Bulandshahr', 'Uttar Pradesh', 'Uttar Pradesh'),
    '208': ('Kanpur', 'Kanpur', 'Uttar Pradesh'),
    '211': ('Prayagraj (Allahabad)', 'Prayagraj', 'Uttar Pradesh'),
    '221': ('Varanasi', 'Varanasi', 'Uttar Pradesh'),
    '226': ('Lucknow', 'Lucknow', 'Uttar Pradesh'),
    '243': ('Bareilly', 'Bareilly', 'Uttar Pradesh'),
    '248': ('Dehradun', 'Dehradun', 'Uttarakhand'),
    '250': ('Meerut', 'Meerut (NCR)', 'Uttar Pradesh'),
    '263': ('Nainital', 'Uttarakhand', 'Uttarakhand'),

    # Western India
    '302': ('Jaipur', 'Jaipur', 'Rajasthan'),
    '303': ('Jaipur Rural', 'Jaipur', 'Rajasthan'),
    '305': ('Ajmer', 'Ajmer', 'Rajasthan'),
    '313': ('Udaipur', 'Udaipur', 'Rajasthan'),
    '324': ('Kota', 'Kota', 'Rajasthan'),
    '342': ('Jodhpur', 'Jodhpur', 'Rajasthan'),
    '380': ('Ahmedabad', 'Ahmedabad', 'Gujarat'),
    '382': ('Gandhinagar / AHD', 'Ahmedabad / Gandhinagar', 'Gujarat'),
    '390': ('Vadodara', 'Vadodara', 'Gujarat'),
    '395': ('Surat', 'Surat', 'Gujarat'),
    '396': ('Valsad / Navsari', 'Gujarat', 'Gujarat'),

    # Maharashtra & Central
    '400': ('Mumbai City / Suburbs', 'Mumbai (MMR)', 'Maharashtra'),
    '401': ('Thane / Palghar / Mira Road', 'Mumbai (MMR)', 'Maharashtra'),
    '411': ('Pune', 'Pune', 'Maharashtra'),
    '412': ('Pune Rural', 'Pune', 'Maharashtra'),
    '413': ('Solapur / Satara', 'Maharashtra', 'Maharashtra'),
    '414': ('Ahmednagar', 'Maharashtra', 'Maharashtra'),
    '416': ('Kolhapur', 'Kolhapur', 'Maharashtra'),
    '421': ('Kalyan / Dombivli / Thane', 'Mumbai (MMR)', 'Maharashtra'),
    '422': ('Nashik', 'Nashik', 'Maharashtra'),
    '425': ('Jalgaon', 'Maharashtra', 'Maharashtra'),
    '431': ('Chhatrapati Sambhajinagar (Aurangabad)', 'Aurangabad', 'Maharashtra'),
    '440': ('Nagpur', 'Nagpur', 'Maharashtra'),
    '452': ('Indore', 'Indore', 'Madhya Pradesh'),
    '462': ('Bhopal', 'Bhopal', 'Madhya Pradesh'),
    '492': ('Raipur', 'Raipur', 'Chhattisgarh'),

    # Southern India
    '500': ('Hyderabad / Secunderabad', 'Hyderabad', 'Telangana'),
    '501': ('Rangareddy', 'Hyderabad', 'Telangana'),
    '502': ('Medak / Sangareddy', 'Hyderabad', 'Telangana'),
    '503': ('Nizamabad', 'Telangana', 'Telangana'),
    '505': ('Karimnagar', 'Telangana', 'Telangana'),
    '506': ('Warangal', 'Warangal', 'Telangana'),
    '520': ('Vijayawada', 'Vijayawada', 'Andhra Pradesh'),
    '530': ('Visakhapatnam', 'Visakhapatnam', 'Andhra Pradesh'),
    '560': ('Bengaluru Urban', 'Bengaluru', 'Karnataka'),
    '561': ('Bengaluru Rural', 'Bengaluru', 'Karnataka'),
    '562': ('Ramanagara / Chikkaballapura', 'Bengaluru', 'Karnataka'),
    '570': ('Mysuru', 'Mysuru', 'Karnataka'),
    '575': ('Mangaluru', 'Mangaluru', 'Karnataka'),
    '580': ('Hubballi-Dharwad', 'Karnataka', 'Karnataka'),
    '590': ('Belagavi', 'Karnataka', 'Karnataka'),
    '600': ('Chennai', 'Chennai', 'Tamil Nadu'),
    '601': ('Thiruvallur', 'Chennai Region', 'Tamil Nadu'),
    '602': ('Kanchipuram', 'Chennai Region', 'Tamil Nadu'),
    '603': ('Chengalpattu', 'Chennai Region', 'Tamil Nadu'),
    '620': ('Tiruchirappalli', 'Tiruchirappalli', 'Tamil Nadu'),
    '625': ('Madurai', 'Madurai', 'Tamil Nadu'),
    '641': ('Coimbatore', 'Coimbatore', 'Tamil Nadu'),
    '670': ('Kannur', 'Kerala', 'Kerala'),
    '673': ('Kozhikode', 'Kozhikode', 'Kerala'),
    '682': ('Kochi / Ernakulam', 'Kochi', 'Kerala'),
    '695': ('Thiruvananthapuram', 'Thiruvananthapuram', 'Kerala'),

    # Eastern & North East
    '700': ('Kolkata', 'Kolkata', 'West Bengal'),
    '711': ('Howrah', 'Kolkata Region', 'West Bengal'),
    '734': ('Siliguri / Darjeeling', 'Siliguri', 'West Bengal'),
    '751': ('Bhubaneswar', 'Bhubaneswar', 'Odisha'),
    '753': ('Cuttack', 'Odisha', 'Odisha'),
    '781': ('Guwahati', 'Guwahati', 'Assam'),
    '788': ('Silchar', 'Assam', 'Assam'),
    '797': ('Kohima / Nagaland', 'Nagaland', 'Nagaland'),
    '799': ('Agartala', 'Tripura', 'Tripura'),
    '800': ('Patna', 'Patna', 'Bihar'),
    '834': ('Ranchi', 'Ranchi', 'Jharkhand'),
    '831': ('Jamshedpur', 'Jamshedpur', 'Jharkhand')
}

# 2-Digit Fallbacks
PREFIX_2DIGIT = {
    '11': ('Delhi', 'Delhi (NCR)', 'Delhi'),
    '12': ('Haryana (Gurugram/Faridabad)', 'Delhi / NCR', 'Haryana'),
    '13': ('Haryana', 'North Region', 'Haryana'),
    '14': ('Punjab', 'Punjab', 'Punjab'),
    '15': ('Punjab', 'Punjab', 'Punjab'),
    '16': ('Chandigarh / PB', 'Chandigarh', 'Punjab'),
    '17': ('Himachal Pradesh', 'Himachal Pradesh', 'Himachal Pradesh'),
    '18': ('Jammu & Kashmir', 'Jammu & Kashmir', 'J&K'),
    '19': ('Kashmir Valley', 'Jammu & Kashmir', 'J&K'),
    '20': ('Noida / Ghaziabad / UP', 'Delhi / NCR', 'Uttar Pradesh'),
    '21': ('Allahabad / Central UP', 'Uttar Pradesh', 'Uttar Pradesh'),
    '22': ('Lucknow / Eastern UP', 'Uttar Pradesh', 'Uttar Pradesh'),
    '23': ('Eastern UP', 'Uttar Pradesh', 'Uttar Pradesh'),
    '24': ('Bareilly / Western UP', 'Uttar Pradesh', 'Uttar Pradesh'),
    '25': ('Meerut / Western UP', 'Uttar Pradesh', 'Uttar Pradesh'),
    '26': ('Uttarakhand', 'Uttarakhand', 'Uttarakhand'),
    '27': ('Gorakhpur / Eastern UP', 'Uttar Pradesh', 'Uttar Pradesh'),
    '28': ('Agra / Mathura', 'Uttar Pradesh', 'Uttar Pradesh'),
    '30': ('Jaipur / Rajasthan', 'Rajasthan', 'Rajasthan'),
    '31': ('Udaipur / S. Rajasthan', 'Rajasthan', 'Rajasthan'),
    '32': ('Kota / E. Rajasthan', 'Rajasthan', 'Rajasthan'),
    '33': ('Bikaner / N. Rajasthan', 'Rajasthan', 'Rajasthan'),
    '34': ('Jodhpur / W. Rajasthan', 'Rajasthan', 'Rajasthan'),
    '36': ('North Gujarat', 'Gujarat', 'Gujarat'),
    '37': ('Kutch / Gujarat', 'Gujarat', 'Gujarat'),
    '38': ('Ahmedabad / Central GJ', 'Gujarat', 'Gujarat'),
    '39': ('Surat / South GJ', 'Gujarat', 'Gujarat'),
    '40': ('Mumbai / Thane', 'Mumbai (MMR)', 'Maharashtra'),
    '41': ('Pune / W. Maharashtra', 'Pune / MH', 'Maharashtra'),
    '42': ('Kalyan / Nashik / N. MH', 'Maharashtra', 'Maharashtra'),
    '43': ('Aurangabad / Marathwada', 'Maharashtra', 'Maharashtra'),
    '44': ('Nagpur / Vidarbha', 'Maharashtra', 'Maharashtra'),
    '45': ('Indore / SW MP', 'Madhya Pradesh', 'Madhya Pradesh'),
    '46': ('Bhopal / Central MP', 'Madhya Pradesh', 'Madhya Pradesh'),
    '47': ('Gwalior / N. MP', 'Madhya Pradesh', 'Madhya Pradesh'),
    '48': ('Jabalpur / E. MP', 'Madhya Pradesh', 'Madhya Pradesh'),
    '49': ('Raipur / Chhattisgarh', 'Chhattisgarh', 'Chhattisgarh'),
    '50': ('Hyderabad / Telangana', 'Hyderabad', 'Telangana'),
    '51': ('Rayalaseema / AP', 'Andhra Pradesh', 'Andhra Pradesh'),
    '52': ('Coastal AP (Vijayawada)', 'Andhra Pradesh', 'Andhra Pradesh'),
    '53': ('Visakhapatnam / N. AP', 'Andhra Pradesh', 'Andhra Pradesh'),
    '56': ('Bengaluru', 'Bengaluru', 'Karnataka'),
    '57': ('Mysuru / S. Karnataka', 'Karnataka', 'Karnataka'),
    '58': ('Hubballi / N. Karnataka', 'Karnataka', 'Karnataka'),
    '59': ('Belagavi / NW Karnataka', 'Karnataka', 'Karnataka'),
    '60': ('Chennai', 'Chennai', 'Tamil Nadu'),
    '61': ('Thanjavur / E. TN', 'Tamil Nadu', 'Tamil Nadu'),
    '62': ('Madurai / S. TN', 'Tamil Nadu', 'Tamil Nadu'),
    '63': ('Salem / Central TN', 'Tamil Nadu', 'Tamil Nadu'),
    '64': ('Coimbatore / W. TN', 'Tamil Nadu', 'Tamil Nadu'),
    '67': ('N. Kerala (Kozhikode)', 'Kerala', 'Kerala'),
    '68': ('Central Kerala (Kochi)', 'Kerala', 'Kerala'),
    '69': ('S. Kerala (Trivandrum)', 'Kerala', 'Kerala'),
    '70': ('Kolkata', 'Kolkata', 'West Bengal'),
    '71': ('Howrah / Hooghly', 'Kolkata Region', 'West Bengal'),
    '72': ('Medinipur / S. WB', 'West Bengal', 'West Bengal'),
    '73': ('Siliguri / N. WB', 'West Bengal', 'West Bengal'),
    '74': ('Nadia / Murshidabad', 'West Bengal', 'West Bengal'),
    '75': ('Bhubaneswar / Odisha', 'Odisha', 'Odisha'),
    '76': ('S. Odisha', 'Odisha', 'Odisha'),
    '77': ('N. Odisha', 'Odisha', 'Odisha'),
    '78': ('Guwahati / Assam', 'Assam / NE', 'Assam'),
    '79': ('North East States', 'North East', 'NE States'),
    '80': ('Patna / Bihar', 'Bihar', 'Bihar'),
    '81': ('Bhagalpur / E. Bihar', 'Bihar', 'Bihar'),
    '82': ('Dhanbad / N. Jharkhand', 'Jharkhand', 'Jharkhand'),
    '83': ('Ranchi / S. Jharkhand', 'Jharkhand', 'Jharkhand'),
    '84': ('Muzaffarpur / N. Bihar', 'Bihar', 'Bihar'),
    '85': ('Purnea / E. Bihar', 'Bihar', 'Bihar')
}

def resolve_pin(pin):
    if not pin or pin == '000000' or pin == 'N/A' or len(pin) < 6:
        return {'district': 'N/A', 'city': 'Unknown / Missing', 'state': 'N/A', 'locality': 'N/A'}

    p3 = pin[:3]
    if p3 in PINCODE_LOOKUP:
        dist, city, state = PINCODE_LOOKUP[p3]
        return {'district': dist, 'city': city, 'state': state, 'locality': f'PIN {pin}'}

    p2 = pin[:2]
    if p2 in PREFIX_2DIGIT:
        dist, city, state = PREFIX_2DIGIT[p2]
        return {'district': dist, 'city': city, 'state': state, 'locality': f'PIN {pin}'}

    return {'district': 'Other India', 'city': 'Other City', 'state': 'India', 'locality': f'PIN {pin}'}

def main():
    csv_path = r'c:\Users\test\Videos\Office\data\kuri-users-2026-08-19.csv'
    cache_path = r'c:\Users\test\Videos\Office\data\pincode_cache.json'

    df = pd.read_csv(csv_path)
    pins = df['pincode'].fillna(0).astype(int).astype(str).str.zfill(6).unique()

    cache = {}
    for p in pins:
        cache[p] = resolve_pin(p)

    os.makedirs(os.path.dirname(cache_path), exist_ok=True)
    with open(cache_path, 'w', encoding='utf-8') as f:
        json.dump(cache, f, indent=2)

    print(f"Offline pincode map created successfully for all {len(cache)} unique pincodes.")

if __name__ == '__main__':
    main()
