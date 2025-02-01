"""
Test class for validating time-related functionality in the models.

This test class utilizes the unittest framework and the freezegun library to ensure that time-related operations in the
models function as expected.

- The `setUp` method freezes time to '2024-01-01' and initializes an Post instance for testing.
- The `test_time_model` method checks the behavior of timestamps during creation, modification, and saving.
  - It asserts that both the creation and modification timestamps are initially set to the frozen time.
  - It updates the post's title, saves the changes, and asserts that the creation timestamp remains unchanged.
  - Finally, it verifies that the modified timestamp reflects the current time after the save operation.

Note: The `create_dummy_post` method from the 'helpers' module is assumed to correctly create Post instances
for testing purposes.

This test suite helps ensure the proper functioning of time-related features in the models, providing
confidence in the reliability and accuracy of the model's temporal behavior.
"""

import datetime
import freezegun

from django import test

from content_rating import models as content_rating_models
from helpers.tests import factory


class TestTimeModel(test.TestCase):
    @freezegun.freeze_time("2024-01-01")
    def setUp(self) -> None:
        """
        Set up the test environment by freezing time and creating an post instance.
        """
        self.post: content_rating_models.Post = factory.create_dummy_post(
            title="title for test", content="content for testing."
        )

    def test_time_model(self) -> None:
        """
        Test the time-related functionality of the Post model.
        """
        # Assert that both the creation and modification timestamps are initially set to the frozen time
        self.assertEqual(self.post.created.strftime("%Y-%m-%d"), "2024-01-01")
        self.assertEqual(self.post.modified.strftime("%Y-%m-%d"), "2024-01-01")

        # Update the post's title and save changes
        self.post.title = "new test title"
        self.post.save()

        # Assert that the creation timestamp remains unchanged
        self.assertEqual(self.post.created.strftime("%Y-%m-%d"), "2024-01-01")

        # Verify that the modified timestamp reflects the current time after the save operation
        self.assertEqual(
            self.post.modified.strftime("%Y-%m-%d"),
            datetime.datetime.now().strftime("%Y-%m-%d"),
        )
