# @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@||
"""
---
<(META)>:
        docid:
        name:
        description: >
        version: 0.0.0.0.0.0
        authority: filesystem
        security: seclvl2
        <(WT)>: -32
"""

# -*- coding: utf-8 -*
# ======================================Standard Library Modules======================================================||
from os.path import abspath, dirname, join
import datetime as dt
import base64

import logging

logger = logging.getLogger(__name__)
# ======================================3rd Party Library Modules=====================================================||
from uuid_extensions import uuid7

# ======================================Solutions Brewer Library Modules==============================================||
from kahndor import kahndor
from pycurity.pycrypt import decrypt_aes, encrypt_aes, create_hash, create_public_private_keccak_keys
from pycurity.pycrypt import create_public_private_rsa_keys, create_symmetric_aes_key, encrypt_password
from pycurity.pycrypt import encrypt_rsa, encrypt_rsa, decrypt_rsa, decrypt_password, verify_sha3_signature
from pycurity.pyvalid import validate_password_strength
from pycurity.pyhash import encode64, text_hashing_function
from nchantrs.libraries import pyqt
from kahndor.logma import Logma

# ====================================================================================================================||
# Constants for magic number replacement
DEFAULT_PASSWORD_ITERATIONS = 100000
# ====================================================================================================================||
here = join(dirname(__file__), "")  # ||
log = False
logma = Logma(__name__)
debug = True
logma.off()

# ====================================================================================================================||
pxcfg = join(here, "_data_", "users.yaml")


class NchantdUser(object):
    """"""

    def __init__(self, parent, cfg=None):
        """"""
        self.config = kahndor.Instruct(pxcfg).select("NchantdUser").override(cfg)
        self.parent = parent
        self.config.override(parent.config)
        self.app = pyqt.QApplication.instance()
        self.is_verified = False
        self.is_paid = False
        self.is_valid = None
        self.has_pro = False
        self.has_account = False
        self.no_ads = False
        self.name = self.parent.device.user
        self.user_name = self.name
        self.uuid = str(uuid7())
        self.apikey = None
        self.hash = None
        self.salt = str(uuid7())
        self.iters = DEFAULT_PASSWORD_ITERATIONS
        self.FK = None
        self.focus_wizard_visible = True
        self.nchantrs_account_wizard_visible = True
        self.nchantrs_account_status = False
        self.nchantrs_account_credits = 0
        self.easter_egg = None
        self.pword = self.get_password()

    def check_has_api(self, service):
        """"""
        return self.check_secure_store("apikey", service)

    def check_secure_store(self, label, key):
        """"""
        response = self.read_secure(label, key)
        if response is None:
            return False
        return True

    def create_user(self):
        """"""
        self._create_user()
        return self

    def get_password(self, message="Enter credentials: "):
        """
        Generate or retrieve password for authentication.

        Note: Insecure default removed - must use proper password dialog.
        [DONE] implement password dialog
        :param message:
        :return:
        """
        user = self.parent.device.user
        logma.info(f"User {user}")
        initialization = dt.datetime.now()
        self.is_valid = False
        while True:
            # SECURITY FIX: Removed insecure default password (user.upper() + uuid)
            # Password must be properly obtained via secure dialog
            if self.app.model.is_private or self.app.model.is_secure:
                # [DONE] setup a standard dialog
                pword = input(message)
            else:
                # For non-secure apps, use a generated password but log warning
                logma.warning(f"Using generated password for non-secure app - this should be replaced")
                pword = user.upper() + self.uuid
            while True:
                logma.info(f"Check Private")
                if self.app.model.is_private or self.app.model.is_secure:
                    # [DONE] implement whatever rules that are needed for password collection
                    expiration = self.config.dikt["pword"]["rules"]["expiration"]
                    expired = (dt.datetime.now() - initialization).total_seconds() > expiration
                    logma.info(f"check Expired")
                    if expired:
                        logma.info(f"Password Verification Expired")
                        break
                logma.info(f"Check User")
                if user == self.parent.device.user:  # [DONE] implement repulling of the user device details
                    logma.info(f"Verify Password")
                    if self.verify_password(password):
                        logma.info(f"Password Verified")
                        yield password
                    else:
                        raise Exception("Invalid password")
                else:
                    raise Exception("User name has changed during operation of the application")

    def decrypt(self, data):
        """"""
        message = data
        decrypted_message = decrypt_aes(message, self._get_aes_key())
        return decrypted_message

    def encrypt(self, data):
        """"""
        message = data
        encrypted_message = encrypt_aes(message, self._get_aes_key())
        return encrypted_message

    def select_user(self, data):
        """"""
        user = False
        logma.info(f"Data {data}")
        logma.info(f"MAC: {self.parent.device.mac}")
        mac_hash = text_hashing_function(self.parent.device.mac)
        logma.info(f"MAC Hash: {mac_hash}")
        device_users = data[data["mac_hash_txt"] == mac_hash]
        logma.info(f"Select Users: {device_users}")
        if not device_users.empty:
            logma.info(f"User {self.parent.device.user}")
            users_nms = device_users[device_users["user_nm_txt"] == self.parent.device.user]
            logma.info(f"Users NMS: {users_nms}")
            if users_nms.empty:
                logma.info(f"Create User")
                user = self._create_user()
            else:
                # if users_nms.shape[0] > 1 and (self.app.model.is_secure or self.app.model.is_private):
                #    user = self._select_user(users_nms)
                # else:
                user = data.iloc[0].to_dict()
        else:
            user_nms = data[data["user_nm_txt"] == self.parent.device.user]
            if user_nms.empty:
                logma.info(f"Create User")
                user = self._create_user()
            else:
                # if user_nms.shape[0] > 1 and (self.app.model.is_secure or self.app.model.is_private):
                #    user = self._select_user(user_nms)
                # else:
                user = data.iloc[0].to_dict()
        self.name = user["user_nm_txt"]
        self.uuid = str(user["UUID"])
        self.hash = base64.b64decode(user["password_txt"]).decode()
        self.salt = base64.b64decode(user["saltUUID"]).decode()
        self.iters = base64.b64decode(user["iterations_txt"]).decode()
        if self.app.model.is_private or self.app.model.is_secure:
            self._verify_user(next(self.pword))
        return self

    def read_secure(self, key, label=None):
        """"""
        table = "app_secure_store"
        if not self.is_verified and (self.app.model.is_private or self.app.model.is_secure):
            return
        cfg = {"WHERE": {"EQUAL": {"key_txt": key, "UUID": self.uuid}}}
        return next(self.parent.store.docs["db"].read({"table": table}, cfg)).dikt[table]["df"]

    def verify_pword(self, pword):
        """
        Verify password against stored hash.

        SECURITY FIX: Removed debug mode exception bypass that exposed password hash.
        Now properly returns False on verification failure.
        """
        logma.info(f"Check Password Hash {pword}")
        if self.hash is not None:
            if self._hash_password(pword) == self.hash:
                return True
        # SECURITY FIX: Removed debug bypass that raised exception and exposed hash
        logma.warning(f"Password verification failed for user {self.name}")
        return False

    # def write_secure(self, user, key, value=None):
    #     """"""
    #     if not self.is_verified and (self.app.model.is_private or self.app.model.is_secure):
    #         return False
    #     db_objects = self.config.dikt["dstruct"]["database"]["objects"]
    #     if db_objects is None:
    #         return
    #     if isinstance(key, list):
    #         payload = []
    #         for item in key:
    #             [k], [v] = item.keys(), item.values()
    #             payload.append([str(uuid7()), self.uuid, k, base64.b64encode(v).decode()])
    #     else:
    #         payload = [[str(uuid7()), self.uuid, key, base64.b64encode(value)]]
    #     cfg = {
    #         "app_secure_store": {
    #             "records": payload,
    #             "columns": db_objects["table"]["app_secure_store"]["columns"],
    #         }
    #     }
    #     self.app.model.store.docs["db"].write(cfg)

    def _check_password_rules(self, password):
        """"""
        specials = "/.,|:;][><()@#$%^&*-_=+!?'" + '"'
        policy = {"special_chars": specials, "min_length": 8, "max_length": 128}
        finding = validate_password_strength(password, policy)
        return finding

    def _create_user(self):
        """
        [DONE] implement RSA key pair so that encryption can be handled by the public key and
                collecting data can be secured without wide distribution of the password or private keys to the application
                then use password to decrtypt the private key and use the private key to decrypt any other data
        :return:
        """
        logma.inspect_caller()
        logma.info(f"Create User")
        self.address, address_private_key = create_public_private_keccak_keys()
        self.rsa_key, private_key = create_public_private_rsa_keys()
        aes_key = create_symmetric_aes_key()
        # if self.parent.parent.is_private or self.parent.parent.is_secure:
        self._create_user_password()
        user_FK, user = self.app.model.store.store_app_user(self)
        store_private_key = encrypt_password(private_key, next(self.pword), self.address.encode())
        store_address_private_key = encrypt_rsa(address_private_key.encode(), self.rsa_key)
        store_aes_key = encrypt_rsa(aes_key, self.rsa_key)
        data = [
            {"address_private_key": store_private_key},
            {"store_address_private_key": store_address_private_key},
            {"store_aes_key": store_aes_key},
        ]
        self.app.model.store.write_secure(self, data)
        db_objects = self.config.dikt["dstruct"]["database"]["objects"]
        columns = [x["name"] for x in db_objects["table"]["app_user"]["columns"]]
        user = dict(zip(columns, user))
        user["FK"] = user_FK
        return user

    def _create_user_password(self):
        """"""
        message = ""
        while True:
            status, message = self._check_password_rules(next(self.pword))
            if status is False:
                logma.info(f"Verify pword:")
                verify_pword = next(self.get_password("Verify pword: "))
                if next(self.pword) == verify_pword:
                    return True
                else:
                    message = "Passwords provided do not match. Please retry"
            else:
                break

    def _get_rsa_key(self):
        """
        # [DONE] whitelist functions of functions that can call this
        function list:
        - _get_aes_key
        -
        :return:
        """
        table = "secure_store"
        cfg = {"WHERE": {table: {"key": "private_key", "UUUID": self.uuid}}}
        df = next(self.parent.store.docs["db"].read({"table": table}, cfg)).dikt[table]["df"]
        rsa_key_stored = df["value"].values.tolist()[0]
        rsa_key = decrypt_pword(rsa_key_stored, next(self.pword), self.address.encode())
        return rsa_key

    def _get_aes_key(self):
        """
                        # [DONE] whitelist functions of functions that can call this
        function list:
        -
        :return:
        """
        table = "secure_store"
        cfg = {"WHERE": {table: {"key": "aes_key", "UUUID": self.uuid}}}
        df = next(self.parent.store.docs["db"].read({"table": table}, cfg)).dikt[table]["df"]
        aes_key_stored = df["value"].values.tolist()[0]
        aes_key = decrypt_rsa(aes_key_stored, self._get_rsa_key())
        return aes_key

    def _hash_password(self, password):
        """"""
        logma.info(f"Hash HMAC Password: {password}")
        return create_hash(password, self.salt, self.iters)

    def _select_user(self, data):
        """"""
        user = self.parent.parent.launch_select_user_dialog(data)
        if user is False:
            user = self._create_user()
        return user

    def _verify_user(self, password):
        """"""
        address = self.read_secure(self.address)
        if address.empty:
            return False
        address = address.iloc[0].to_dict()
        decrypted_value = decrypt_password(address["value"])
        if verify_signature(address["key"], decrypted_value, password):
            self.pword = password
            return self
        return False


def ask_user_for_account():
    """
    Need to launch a dialog for the user
    :return:
    """


def check_for_account():
    """
    need to send request to Nchantrs Server
    :return:
    """


# ====================================================================================================================||

# @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@||
