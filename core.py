from validate_email_address import validate_email
from termcolor import colored
import DNS
import json
import time
import os
os.system('color')


def validate_email_address(email):
    status = validate_email(str(email).strip(), verify=True)
    return status


def update_dealers_email_addresses():
    DNS.defaults['server'] = ['8.8.8.8', '8.8.4.4']
    file_name = 'all_dealers.json'

    with open(file_name, 'r') as f:
        data = json.load(f)

    start_range = 0
    end_range = len(data['Accounts list'])

    all_dealers_file = []
    total_addresses_checked = 0
    real_addresses = 0

    print('                 ')
    print('Checking the emails up to cardealer ' + str(end_range))

    for i in range(start_range, end_range):
        if not int(i) == 0:
            if int(i) % 100 == 0:
                print('')
                print(colored('Checked ' + str(total_addresses_checked) + ' emails so far. Fund ' + str(real_addresses) +
                    ' real emails, which means ' + str(float(real_addresses/total_addresses_checked*100)) + '%', 'yellow'))
                print('')

        print('-----------------')
        print('Checking dealer: ' + str(i))
        dealer_new_data = {}
        email_list = ['email_1', 'email_2', 'email_3', 'email_4']
        dealer_data = data['Accounts list'][i]
        dealer_name = dealer_data['legal_name']
        dealer_website = dealer_data['website_address']
        dealer_user = dealer_data['account']['username']
        dealer_password = dealer_data['account']['password']

        dealer_new_data['legal_name'] = dealer_name
        dealer_new_data['username'] = dealer_user
        dealer_new_data['password'] = dealer_password

        dealer_new_data['emails'] = {}

        for item in email_list:
            try:
                if (not dealer_data[item] == '') or (not 'no-email' in dealer_data[item]) or (not 'not any' in dealer_data[item]):
                    is_valid = validate_email_address(dealer_data[item])
                    total_addresses_checked += 1
                    if is_valid == True:
                        dealer_new_data['emails'][item] = dealer_data[item]
                        print(
                            colored(str(dealer_data[item]) + ' is valid', 'green'))
                        real_addresses += 1
                    else:
                        print(
                            colored(str(dealer_data[item]) + ' is not valid', 'red'))
            except KeyError:
                continue
        if (not dealer_website == '') or (not dealer_website == ' '):
            total_addresses_checked += 1
            new_email = 'contact@' + dealer_website
            new_validated_email = validate_email_address(new_email)
            if new_validated_email == True:
                dealer_new_data['emails']['new_email'] = new_email
                print(colored(str(new_email) + ' is valid', 'green'))
                real_addresses += 1
            else:
                print(colored(str(new_email) + ' is not valid', 'red'))

        all_dealers_file.append(dealer_new_data)
        file_name = 'all-dealers-edit.json'

        with open(file_name, 'w') as outfile:
            json.dump(all_dealers_file, outfile)
        time.sleep(0.1)
        print('Done!')
        print('                 ')

    print('Checked ' + str(total_addresses_checked) + ' emails. Fund ' + str(real_addresses) +
          ' real emails, which means ' + str(float(real_addresses/total_addresses_checked*100)) + '%')
    print('')
