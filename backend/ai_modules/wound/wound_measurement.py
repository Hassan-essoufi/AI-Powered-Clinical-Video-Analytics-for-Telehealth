import numpy as np

class WoundMeasurement:
    """
    Prend le masque binaire de WoundSegmenter et calcule :
    - Surface de la plaie en cm²  (avec objet de référence pour l'échelle)
    - Composition couleur         (distribution RGB pour détecter l'infection)

    Indicateurs d'infection :
        Rouge/jaune intense → inflammation
        Noir/marron foncé   → nécrose (tissu mort)
        Verdâtre            → infection possible
        Rose/rouge clair    → cicatrisation normale
    """

    def __init__(self, pixels_per_cm: float = None):
        """
        Args:
            pixels_per_cm: facteur d'échelle — calibré avec un objet de référence.
        """
        self.pixels_per_cm = pixels_per_cm

    def measure(self, frame: np.ndarray, mask: np.ndarray) -> dict:
        """
        Méthode principale — calcule surface et composition couleur de la plaie.

        Args:
            frame : numpy array (H, W, 3) — frame BGR originale
            mask  : numpy array binaire (H, W) depuis WoundSegmenter

        Returns:
            dict avec area_cm2, color_composition, infection_risk
        """
        area_px           = self._compute_area_pixels(mask)
        area_cm2          = self._convert_to_cm2(area_px)
        color_composition = self._analyze_color(frame, mask)
        infection_risk    = self._assess_infection(color_composition)

        return {
            "area_pixels"      : area_px,
            "area_cm2"         : area_cm2,
            "color_composition": color_composition,
            "infection_risk"   : infection_risk,
            "status"           : "live"
        }

    def _compute_area_pixels(self, mask: np.ndarray) -> int:
        """Compte le nombre de pixels dans le masque de la plaie."""
        return int(np.sum(mask))

    def _convert_to_cm2(self, area_px: int) -> float:
        """
        Convertit la surface en pixels en cm².

        Nécessite une calibration préalable avec un objet de référence
        (ex: pièce de monnaie de diamètre connu posée à côté de la plaie).
        """
        if self.pixels_per_cm is None:
            return 0.0  # pas encore calibré
        return round(area_px / (self.pixels_per_cm ** 2), 2)

    def _analyze_color(self, frame: np.ndarray, mask: np.ndarray) -> dict:
        """
        Calcule la composition RGB moyenne des pixels dans le masque de la plaie.

        frame est en BGR (format OpenCV) → on inverse pour avoir RGB.
        """
        if np.sum(mask) == 0:
            return {"r_mean": 0.0, "g_mean": 0.0, "b_mean": 0.0}

        # extraire uniquement les pixels de la plaie
        wound_pixels       = frame[mask == 1]           # shape: (N, 3) en BGR
        b_mean, g_mean, r_mean = wound_pixels.mean(axis=0)

        return {
            "r_mean": round(float(r_mean), 2),
            "g_mean": round(float(g_mean), 2),
            "b_mean": round(float(b_mean), 2)
        }

    def _assess_infection(self, color_composition: dict) -> str:
        """
        Évalue le risque d'infection basé sur la composition couleur.

        Seuils basés sur des indicateurs cliniques visuels :
        - Rouge intense (r > 180, g < 80)  → inflammation élevée
        - Verdâtre (g > r et g > b)        → infection possible
        - Très sombre (tout < 80)          → nécrose possible
        - Autrement                         → risque faible
        """
        r = color_composition["r_mean"]
        g = color_composition["g_mean"]
        b = color_composition["b_mean"]

        if r > 180 and g < 80:
            return "high"      # rouge intense → inflammation
        elif g > r and g > b:
            return "medium"    # verdâtre → infection possible
        elif r < 80 and g < 80 and b < 80:
            return "high"      # très sombre → nécrose possible
        else:
            return "low"       # couleurs normales → cicatrisation

    def calibrate(self, reference_diameter_cm: float, reference_diameter_px: int):
        """
        Définit le facteur pixels_per_cm via un objet de référence.

        Args:
            reference_diameter_cm : taille réelle de l'objet (ex: 2.6cm pour une pièce)
            reference_diameter_px : taille en pixels du même objet dans la frame
        """
        self.pixels_per_cm = reference_diameter_px / reference_diameter_cm