from ldap3 import Server, Connection, ALL
from ldap3.core.exceptions import LDAPException, LDAPBindError
import base64
import shutil

from pg_db import insert_ad_users_new

AD_SEARCH_TREE = "ou=,dc=,dc=local"
AD_SEARCH_TREE2 = "ou=,ou=,dc=,dc=local"
AD_SEARCH_TREE3 = "ou=,ou=,dc=,dc=local"


def ad_search_by_objectguid(tabnumber):
    server = Server('10.45.10.9', get_info=ALL)
    conn = Connection(server, user="hju\\cucm_user", password="@111111", auto_bind=True)
    print('LDAP Bind Successful.')
    print(tabnumber)
    adFltr = '(&(sAMAccountName=' + tabnumber + ')(objectClass = person)(physicalDeliveryOfficeName=*)(!(UserAccountControl:1.2.840.113556.1.4.803:=2))(!(objectClass = computer)))'
    conn.search(AD_SEARCH_TREE, adFltr, attributes=['sAMAccountName', 'description', 'cn', 'telephoneNumber', 'mobile', 'mail', 'title', 'department'])
    return_list = []
    for entry in conn.response:
        try:
            return_list.append(entry['attributes'])
        except KeyError:
            continue

    print(entry.get('attributes', {}).get('sAMAccountName', ''))
    tabnumbertest = entry.get('attributes', {}).get('cn', '')
    # return return_list
    return tabnumbertest


def ad_search_all():
    server = Server('10.45.50.9', get_info=ALL)
    conn = Connection(server, user="-\\", password="CvVm", auto_bind=True)
    print('LDAP Bind Successful.')
    # adFltr = '(&(objectClass = person)(physicalDeliveryOfficeName=*)(!(UserAccountControl:1.2.840.113556.1.4.803:=2))(!(objectClass = computer)))'
    adFltr = '(&(objectClass = person)(!(UserAccountControl:1.2.840.113556.1.4.803:=2))(!(objectClass = computer))(company=Филиал ))'
    adFltrAP = '(&(objectClass = person)(!(UserAccountControl:1.2.840.113556.1.4.803:=2))(!(objectClass = computer))(company=Филиал ))'
  
    conn.search(AD_SEARCH_TREE2, adFltr, attributes=['sAMAccountName', 'description', 'cn', 'telephoneNumber', 'mobile', 'mail', 'title', 'department'])
    return_list_all = []
    for entry in conn.response:
        try:
            return_list_all.append(entry['attributes'])
        except KeyError:
            continue

    conn.search(AD_SEARCH_TREE3, adFltr, attributes=['sAMAccountName', 'description', 'cn', 'telephoneNumber', 'mobile', 'mail', 'title', 'department'])

    for entry in conn.response:
        try:
            return_list_all.append(entry['attributes'])
        except KeyError:
            continue

    conn.search(AD_SEARCH_TREE3, adFltrAP, attributes=['sAMAccountName', 'description', 'cn', 'telephoneNumber', 'mobile', 'mail', 'title', 'department'])

    for entry in conn.response:
        try:
            return_list_all.append(entry['attributes'])
        except KeyError:
            continue

    print(type(return_list_all))
    ad_take_photo()
    # insert_ad_users_new(return_list_all)

    # conn.unbind()
    return return_list_all
    # print(return_list[0])


def ad_login_users(adlogin, ldap_password):

    server = Server('10.45.50.9', get_info=ALL)

    connection = Connection(server,
                            user=adlogin,
                            password=ldap_password,
                            auto_bind=True)

    print(f" *** Response from the ldap bind is \n{connection}")


def ad_take_photo():
    server = Server('10.45.50.9', get_info=ALL)
    conn = Connection(server, user="\\", password="Cuuu", auto_bind=True)
    print('LDAP Bind Successful.')
    adFltr = '(&(objectClass = person)(!(UserAccountControl:1.2.840.113556.1.4.803:=2))(!(objectClass = computer)))'
    # adFltr = '(&(objectClass = person)(company=Филиал  )(!(UserAccountControl:1.2.840.113556.1.4.803:=2))(!(objectClass = computer)))'
    # adFltrAP = '(&(objectClass = person)(!(UserAccountControl:1.2.840.113556.1.4.803:=2))(!(objectClass = computer))(company=Филиал ))'
    conn.search(AD_SEARCH_TREE, adFltr, attributes=['thumbnailPhoto', 'sAMAccountName'])
    return_list_all = []
    for entry in conn.response:
        try:
            return_list_all.append(entry['attributes'])
            photo = entry.get('attributes', {}).get('thumbnailPhoto', '')
            tabnumber = entry.get('attributes', {}).get('sAMAccountName', '')
            # if photo  True:
            # humbnailPhoto = base64.b64encode(entry.thumbnailPhoto.value)
            # print(humbnailPhoto)
            if (type(photo) == bytes):
                # print(type(photo))
                photo_encoded = base64.b64encode(photo)
                # print(photo_encoded)

                image_binary = base64.decodebytes(photo_encoded)
                with open("static/photo/" + tabnumber + '.jpeg', 'wb') as f:
                    f.write(image_binary)
            else:
                print(type(photo))
                shutil.copyfile("static/photo/nophoto.png", "static/photo/" + tabnumber + '.jpeg')
        #     with open("photo/" + tabnumber + '.jpeg', 'wb') as file_to_save:
        #         decoded_image_data = base64.encodebytes(photo_encoded)
        #         file_to_save.write(decoded_image_data)
        # # else:
            #     print("No date")

            # # data = photo_encoded.replace(' ', '+')
            # imgdata = base64.b64decode(photo_encoded)
            # message = imgdata.decode('ascii')
            # filename = conn.response[0].get('attributes', {}).get('sAMAccountName', '') + '.jpg'  
            # with open(filename, 'wb') as f:
            #     f.write(message)

        except KeyError:
            continue
    return


