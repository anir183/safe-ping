from dataclasses import dataclass


@dataclass(frozen=True)
class Images:
	LOGO: str = "icon.png"
	SPLASH_ANDROID: str = "splash_android.png"


@dataclass(frozen=True)
class ImageSizes:
	XS: int = 16
	SM: int = 24
	MD: int = 32
	LG: int = 48
	XL: int = 64
	XXL: int = 96

	AVATAR_SM: int = 32
	AVATAR_MD: int = 48
	AVATAR_LG: int = 72

	ICON_SM: int = 18
	ICON_MD: int = 24
	ICON_LG: int = 32

	LOGO_SM: int = 30
	LOGO_MD: int = 48
	LOGO_LG: int = 72
