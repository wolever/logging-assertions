import logging
import logging.handlers

__version__ = (0, 0, 1)

class LoggingAssertionsError(Exception):
    pass


class LoggingAssertions(object):
    def __init__(self):
        self.handler = None

    def _get_handler(self):
        return logging.handlers.BufferingHandler(1000)

    def _get_formatter(self):
        return logging.Formatter("%(name)s: %(levelname)s: %(message)s")

    def _get_logged_records(self):
        return self.handler.buffer

    def begin_capture(self):
        """ Installs a log handler which will capure log messages during a test.
            The ``logged_messages`` and ``assert_no_errors_logged`` functions can be
            used to make assertions about these logged messages.

            For example::

                from ensi_common.testing import (
                    setup_logging, teardown_logging, assert_no_errors_logged,
                    assert_logged,
                )

                class TestWidget(object):
                    def setup(self):
                        setup_logging()

                    def teardown(self):
                        assert_no_errors_logged()
                        teardown_logging()

                    def test_that_will_fail(self):
                        log.warning("this warning message will trigger a failure")

                    def test_that_will_pass(self):
                        log.info("but info messages are ok")
                        assert_logged("info messages are ok")
            """
                        
        root_logger = logging.getLogger()
        if self.handler is not None:
            root_logger.removeHandler(self.handler)
        self.handler.setFormatter(self._get_formatter())
        root_logger.addHandler(self.handler)

    def end_capture(self):
        if self.handler is not None:
            logging.getLogger().removeHandler(self.handler)
            self.handler = None

    def get_logged_records(self):
        if not self.handler:
            raise LoggingAssertionsError(
                "Cannot get logged messages because 'begin_capture()' has "
                "not been called. Hint: put a call to 'begin_capture()' in "
                "your test's 'setUp()' method, or subclass the "
                "'LoggingAssertionsMixin' mixin. If you have subclassed "
                "'LoggingAssertionsMixin', make sure it is the *first* "
                "subclass: 'class MyTestCase(LoggingAssertionsMixin, "
                "unittest.TestCase)."
            )
        return self._get_logged_records()

    def get_logged_messages(self):
        return map(self.handler.format, self.get_logged_records())

    def assert_no_errors_logged(self, level=None):
        if level is None:
            level = logging.WARNING
        errors = filter(lambda r: r.levelno >= level, self.get_logged_records())
        if errors:
            raise AssertionError("%d errors were logged: %r" %(
                map(self.handler.format, errors),
            ))

    def assert_logged(self, expected):
        for msg in self.get_logged_messages():
            if expected in msg:
                return
        raise AssertionError("no logged message contains %r"
                             %(expected, ))


class LoggingAssertionsMixin(object):
    logging_assertions_cls = LoggingAssertions
    logging_assertions = None

    def setUp(self):
        if self.logging_assertions is None:
            self.logging_assertions = self.logging_assertions_cls()
        self.logging_assertions.begin_capture()
        super(LoggingAssertionsMixin, self).setUp()

    def tearDown(self):
        if self.logging_assertions is not None:
            self.logging_assertions.end_capture()

    def getLoggedRecords(self):
        return self.logging_assertions.get_logged_records()

    def getLoggedMessages(self):
        return self.logging_assertions.get_logged_messages()

    def assertNoErrorsLogged(self, level=None):
        self.logging_assertions.assert_no_errors_logged(level=level)

    def assertLogged(self, expected):
        self.logging_assertions.assert_logged(expected)


logging_assertions = LoggingAssertions()
begin_capture = logging_assertions.begin_capture
end_capture = logging_assertions.end_capture
get_logged_records = logging_assertions.get_logged_records
get_logged_messages = logging_assertions.get_logged_messages
assert_no_errors_logged = logging_assertions.assert_no_errors_logged
assert_logged = logging_assertions.assert_logged
