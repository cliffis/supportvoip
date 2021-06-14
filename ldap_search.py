from ldap3 import Server, Connection, ALL
from ldap3.core.exceptions import LDAPException, LDAPBindError
import base64
import shutil

from pg_db import insert_ad_users_new

AD_SEARCH_TREE = "ou=ASE_HU,dc=ase-hu,dc=local"
AD_SEARCH_TREE2 = "ou=Budapest,ou=ASE_HU,dc=ase-hu,dc=local"
AD_SEARCH_TREE3 = "ou=Paks,ou=ASE_HU,dc=ase-hu,dc=local"


def ad_search_by_objectguid(tabnumber):
    server = Server('10.45.0.9', get_info=ALL)
    conn = Connection(server, user="ase-hu\\cucm_user", password="CvGs@tVm", auto_bind=True)
    print('LDAP Bind Successful.')
    print(tabnumber)
    adFltr = '(&(sAMAccountName=' + tabnumber + ')(objectClass = person)(physicalDeliveryOfficeName=ASE_HU*)(!(UserAccountControl:1.2.840.113556.1.4.803:=2))(!(objectClass = computer)))'
    # adFltr = '(&(sAMAccountName=' + tabnumber + ')(objectclass = person)(!(objectclass = computer))(!(ou=!ASE_Businesstrip_STAFF))(!(UserAccountControl:1.2.840.113556.1.4.803:=2)))'
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
    server = Server('10.45.0.9', get_info=ALL)
    conn = Connection(server, user="ase-hu\\cucm_user", password="CvGs@tVm", auto_bind=True)
    print('LDAP Bind Successful.')
    # adFltr = '(&(objectClass = person)(physicalDeliveryOfficeName=ASE_HU*)(!(UserAccountControl:1.2.840.113556.1.4.803:=2))(!(objectClass = computer)))'
    adFltr = '(&(objectClass = person)(!(UserAccountControl:1.2.840.113556.1.4.803:=2))(!(objectClass = computer))(company=Филиал АО ИК "АСЭ" в Венгрии))'
    adFltrAP = '(&(objectClass = person)(!(UserAccountControl:1.2.840.113556.1.4.803:=2))(!(objectClass = computer))(company=Филиал АО "Атомпроект" в Венгрии))'
    # adFltr = '(&(objectclass = person)(!(objectclass = computer))(!(ou = !ASE_Businesstrip_STAFF))(!(ou = unknown))(!(ou = Service))(!(UserAccountControl:1.2.840.113556.1.4.803:=2)))'
    # (physicalDeliveryOfficeName= *)
    # adFltr = '(&(objectclass = person)(!(objectclass = computer))(!(distinguishedName = ou=!ASE_Businesstrip_STAFF,ou=Office_ASE,ou=Paks,ou=ASE_HU,dc=ase-hu,dc=local))(!(distinguishedName = ou=unknown,ou=Office_ASE,ou=Paks,ou=ASE_HU,dc=ase-hu,dc=local))(!(distinguishedName = ou=Service,ou=ASE_HU,dc=ase-hu,dc=local))(!(UserAccountControl:1.2.840.113556.1.4.803:=2)))'

    # adFltr = '(&(objectclass = person)(distinguishedName = ou=... *,ou=Reception,ou=BankCenter,ou=Budapest,dc=ASE_HU,dc=ase-hu,dc=local))'.format()
    # adFltr = '(&(objectclass = person)(!(objectclass = computer))(!(UserAccountControl:1.2.840.113556.1.4.803:=2)))'{0}*

    # adFltr = '(&(objectclass = person)(!(objectclass = computer))(!(memberOf=ou=!ASE_Businesstrip_STAFF,ou=Office_ASE,ou=Paks,ou=ASE_HU,dc=ase-hu,dc=local))(!(memberOf=ou=unknown,ou=Office_ASE,ou=Paks,ou=ASE_HU,dc=ase-hu,dc=local))(!(memberOf=ou=Service,ou=ASE_HU,dc=ase-hu,dc=local))(!(UserAccountControl:1.2.840.113556.1.4.803:=2)))'
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
    # server = Server('10.45.0.9', get_info=ALL)
#     # try:
#         # conn = Connection(server, user="ase-hu\\seryakov", password="[htyDFV123", auto_bind=True)
#     conn = Connection(server, user=adlogin, password=adpassword, auto_bind=True)
#     print(conn)
#     print('LDAP Bind Successful.')
#     # except:
#         # print(conn.status)
#         print('LDAP Error.')
#     # print('LDAP Bind Successful.')
#     # adFltr = '(&(sAMAccountName=' + tabnumber + ')(objectClass = person)(physicalDeliveryOfficeName=ASE_HU*)(!(UserAccountControl:1.2.840.113556.1.4.803:=2))(!(objectClass = computer)))'
#     # # adFltr = '(&(sAMAccountName=' + tabnumber + ')(objectclass = person)(!(objectclass = computer))(!(ou=!ASE_Businesstrip_STAFF))(!(UserAccountControl:1.2.840.113556.1.4.803:=2)))'
#     # conn.search(AD_SEARCH_TREE, adFltr, attributes=['sAMAccountName', 'description', 'cn', 'telephoneNumber', 'mobile', 'mail', 'title', 'department'])
#     # return_list = []
#     # for entry in conn.response:
#     #     try:
#     #         return_list.append(entry['attributes'])
#     #     except KeyError:
#     #         continue
#     #
#     # print(return_list)
#     return
    server = Server('10.45.0.9', get_info=ALL)

    connection = Connection(server,
                            user=adlogin,
                            password=ldap_password,
                            auto_bind=True)

    print(f" *** Response from the ldap bind is \n{connection}")


def ad_take_photo():
    server = Server('10.45.0.9', get_info=ALL)
    conn = Connection(server, user="ase-hu\\cucm_user", password="CvGs@tVm", auto_bind=True)
    print('LDAP Bind Successful.')
    adFltr = '(&(objectClass = person)(!(UserAccountControl:1.2.840.113556.1.4.803:=2))(!(objectClass = computer)))'
    # adFltr = '(&(objectClass = person)(company=Филиал АО ИК "АСЭ" в Венгрии)(!(UserAccountControl:1.2.840.113556.1.4.803:=2))(!(objectClass = computer)))'
    # adFltrAP = '(&(objectClass = person)(!(UserAccountControl:1.2.840.113556.1.4.803:=2))(!(objectClass = computer))(company=Филиал АО "Атомпроект" в Венгрии))'
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
            # filename = conn.response[0].get('attributes', {}).get('sAMAccountName', '') + '.jpg'  # I assume you have a way of picking unique filenames
            # with open(filename, 'wb') as f:
            #     f.write(message)

        except KeyError:
            continue
    return


# ad_login_users("cucm_user", "CvGs@tVm")

# ad_take_photo()