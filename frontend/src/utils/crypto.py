import base64
import hashlib
import hmac
import os

_SHARED_PASSPHRASE = b"safe-ping-demo-2026"
_PBKDF2_ITERATIONS = 100_000
_SALT_LEN = 16
_IV_LEN = 16
_KEY_LEN = 32
_HMAC_ALGO = "sha256"


def _derive_key(salt: bytes) -> bytes:
	return hashlib.pbkdf2_hmac(
		_HMAC_ALGO, _SHARED_PASSPHRASE, salt, _PBKDF2_ITERATIONS, dklen=_KEY_LEN
	)


def _keystream(key: bytes, iv: bytes, length: int) -> bytes:
	stream = b""
	counter = 0
	while len(stream) < length:
		counter_bytes = counter.to_bytes(16, "big")
		stream += hmac.new(key, iv + counter_bytes, _HMAC_ALGO).digest()
		counter += 1
	return stream[:length]


def encrypt(plaintext: str) -> str:
	salt = os.urandom(_SALT_LEN)
	key = _derive_key(salt)
	iv = os.urandom(_IV_LEN)
	pt = plaintext.encode("utf-8")
	ks = _keystream(key, iv, len(pt))
	ciphertext = bytes(a ^ b for a, b in zip(pt, ks))
	return base64.b64encode(salt + iv + ciphertext).decode("ascii")


def decrypt(encoded: str) -> str:
	raw = base64.b64decode(encoded)
	salt, iv, ciphertext = raw[:_SALT_LEN], raw[_SALT_LEN:_SALT_LEN + _IV_LEN], raw[_SALT_LEN + _IV_LEN:]
	key = _derive_key(salt)
	ks = _keystream(key, iv, len(ciphertext))
	plaintext = bytes(a ^ b for a, b in zip(ciphertext, ks))
	return plaintext.decode("utf-8")
