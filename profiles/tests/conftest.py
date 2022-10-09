# Add fixtures from other conftest.py
from posts.tests.conftest import (client, create_empty_profile,  # noqa: F401
                                  create_test_like, create_test_post,
                                  create_test_user)
