from dataclasses import dataclass

FONT_FILES = {
	"Bricolage Grotesque": "fonts/bricolage_grotesque/BricolageGrotesque-VariableFont_opsz,wdth,wght.ttf",
	"IBM Plex": "fonts/imb_plex/IBMPlexSans-VariableFont_wdth,wght.ttf",
	"IBM Plex Italic": "fonts/imb_plex/IBMPlexSans-Italic-VariableFont_wdth,wght.ttf",
}


@dataclass(frozen=True)
class Fonts:
	HEADER: str = "Bricolage Grotesque"
	BODY: str = "IBM Plex"
	BODY_ITALIC: str = "IBM Plex Italic"


@dataclass(frozen=True)
class FontSize:
	XS: int = 10

	SM: int = 12
	MD: int = 14
	LG: int = 18

	XL: int = 24
	XXL: int = 32
