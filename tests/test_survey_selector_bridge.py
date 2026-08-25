import unittest
from unittest.mock import patch

from philoui.survey import (
    CustomStreamlitSurvey,
    _date_range_picker,
    _dichotomy,
    _qualitative,
    parametric_quantitative,
)


class SelectorBridgeTests(unittest.TestCase):
    def test_dichotomy_keeps_widget_label_separate_from_participant_name(self):
        with patch("philoui.survey._qualitative_selector", return_value="chosen") as selector:
            result = _dichotomy(
                "Confidence",
                name="participant",
                question="Where do you stand?",
                key="dichotomy",
            )

        self.assertEqual(result, "chosen")
        selector.assert_called_once_with(
            component="dichotomy",
            name="participant",
            label="Confidence",
            key="dichotomy",
            height=100,
            question="Where do you stand?",
            rotationAngle=0,
            gradientWidth=40,
            invert=False,
            shift=0,
        )

    def test_qualitative_keeps_widget_label_separate_from_name(self):
        with patch("philoui.survey._qualitative_selector", return_value="inside") as selector:
            result = _qualitative(
                "Region",
                name="Proximity",
                question="Choose a region",
                areas=4,
                data_values=["outside", "inside"],
                key="qualitative",
            )

        self.assertEqual(result, "inside")
        self.assertEqual(selector.call_args.kwargs["label"], "Region")
        self.assertEqual(selector.call_args.kwargs["name"], "Proximity")

    def test_quantitative_keeps_widget_label_separate_from_name(self):
        with patch("philoui.survey._qualitative_selector", return_value="10") as selector:
            result = parametric_quantitative(
                "Amount",
                name="Commitment",
                question="Choose a level",
                data_values=[0, 1, 10],
                key="quantitative",
            )

        self.assertEqual(result, "10")
        self.assertEqual(selector.call_args.kwargs["label"], "Amount")
        self.assertEqual(selector.call_args.kwargs["name"], "Commitment")

    def test_date_range_keeps_widget_label_separate_from_name(self):
        with patch("philoui.survey.date_range_picker", return_value=("start", "end")) as picker:
            result = _date_range_picker(
                "Date range",
                name="Active interval",
                min_date="minimum",
                max_date="maximum",
                error_message="Choose both dates",
                key="date-range",
            )

        self.assertEqual(result, ("start", "end"))
        picker.assert_called_once_with(
            "Active interval",
            default_start=None,
            default_end=None,
            min_date="minimum",
            max_date="maximum",
            error_message="Choose both dates",
            key="date-range",
        )

    def test_survey_date_range_passes_name_as_the_widget_label(self):
        survey = CustomStreamlitSurvey(label="date-regression")
        with patch("philoui.survey.date_range_picker", return_value=None) as picker:
            survey.mandatory_date_range(
                name="Active interval",
                id="active-interval",
                key="active-interval",
            )

        self.assertEqual(picker.call_args.args[0], "Active interval")


if __name__ == "__main__":
    unittest.main()
