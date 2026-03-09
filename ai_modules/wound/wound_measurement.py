"""
wound_measurement.py
--------------------
Sprint 1 : Skeleton — Compute area (cm²) and color composition from wound mask.
Sprint 2 : Will use reference object for real-world scale calibration.
"""

import numpy as np


class WoundMeasurement:
    """
    Takes the binary mask from WoundSegmenter and computes:
    - Wound area in cm²  (using a reference object for scale)
    - Color composition  (RGB distribution to detect infection)

    Infection indicators (Sprint 2):
        - High red/yellow → inflammation
        - Dark/black regions → necrosis
        - Yellow/green → possible infection
    """

    def __init__(self, pixels_per_cm: float = None):
        """
        Args:
            pixels_per_cm: scale factor — set after calibration with reference object.
                           None in Sprint 1 (placeholder).
        """
        self.pixels_per_cm = pixels_per_cm  # calibrated in Sprint 2

    def measure(self, frame: np.ndarray, mask: np.ndarray) -> dict:
        """
        Main method — computes area and color composition of the wound.

        Args:
            frame : numpy array (H, W, 3) — original BGR video frame
            mask  : binary numpy array (H, W) from WoundSegmenter

        Returns:
            dict with area_cm2, color_composition, infection_risk
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
            "status"           : "placeholder_output"  # Sprint 1 marker
        }

    def _compute_area_pixels(self, mask: np.ndarray) -> int:
        """
        Counts the number of pixels in the wound mask.
        """
        return int(np.sum(mask))

    def _convert_to_cm2(self, area_px: int) -> float:
        """
        Converts pixel area to cm² using scale factor.

        Sprint 1 : returns 0.0 (no calibration yet).
        Sprint 2 : use reference object (e.g. coin of known size) to set
                   self.pixels_per_cm, then:
                   return area_px / (self.pixels_per_cm ** 2)
        """
        if self.pixels_per_cm is None:
            return 0.0  # placeholder — calibration not done yet
        return area_px / (self.pixels_per_cm ** 2)

    def _analyze_color(self, frame: np.ndarray, mask: np.ndarray) -> dict:
        """
        Computes the average RGB color composition inside the wound mask.

        Sprint 1 : returns placeholder zeros.
        Sprint 2 : extract masked region and compute color histogram/means.
        """
        if np.sum(mask) == 0:
            return {"r_mean": 0.0, "g_mean": 0.0, "b_mean": 0.0}

        # Sprint 1 : placeholder
        # Sprint 2 :
        #   wound_pixels = frame[mask == 1]       # shape: (N, 3) BGR
        #   b_mean, g_mean, r_mean = wound_pixels.mean(axis=0)
        return {
            "r_mean": 0.0,   # placeholder
            "g_mean": 0.0,   # placeholder
            "b_mean": 0.0    # placeholder
        }

    def _assess_infection(self, color_composition: dict) -> str:
        """
        Estimates infection risk based on color composition.

        Sprint 1 : always returns 'unknown' as placeholder.
        Sprint 2 : apply color thresholds or a trained classifier.
        """
        # TODO Sprint 2 : real infection detection logic
        return "unknown"  # placeholder

    def calibrate(self, reference_diameter_cm: float, reference_diameter_px: int):
        """
        Sets the pixels_per_cm scale using a known reference object.

        Args:
            reference_diameter_cm : real-world size of reference (e.g. 2.6cm for a coin)
            reference_diameter_px : measured pixel size of same reference in frame
        """
        self.pixels_per_cm = reference_diameter_px / reference_diameter_cm
