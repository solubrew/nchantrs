"""Tests for the Nchantrs CLI module."""

from unittest.mock import patch

from nchantrs.cli import (
    DEFAULT_AGENT,
    DEFAULT_AGENT_NAME,
    cmd_actions,
    cmd_config,
    cmd_dialogs,
    cmd_events,
    cmd_extensions,
    cmd_help,
    cmd_install,
    cmd_libraries,
    cmd_library,
    cmd_logging,
    cmd_models,
    cmd_run,
    cmd_services,
    cmd_test,
    cmd_themes,
    cmd_uninstall,
    cmd_updates,
    cmd_utilities,
    cmd_version,
    cmd_views,
    cmd_widgets,
    cmd_wizards,
    create_parser,
    main,
)


class TestCreateParser:
    """Tests for create_parser function."""

    def test_create_parser_returns_argument_parser(self):
        """Test that create_parser returns an ArgumentParser instance."""
        parser = create_parser()
        assert parser is not None
        assert parser.prog == "nchantrs"

    def test_create_parser_has_run_command(self):
        """Test that parser has run subcommand."""
        parser = create_parser()
        {action: None for action in parser._subparsers._actions}
        assert "run" in [sp.dest for sp in parser._subparsers._actions[1].choices.values()]

    def test_create_parser_has_version_flag(self):
        """Test that parser has version flag."""
        parser = create_parser()
        assert any("-v" in action.option_strings for action in parser._actions)


class TestMain:
    """Tests for main function."""

    def test_main_returns_zero(self):
        """Test that main returns 0 on success."""
        result = main()
        assert result == 0

    def test_main_with_custom_agent(self):
        """Test main with custom agent parameter."""
        result = main(agent="custom_agent")
        assert result == 0

    def test_main_with_none_agent(self):
        """Test main with None agent defaults to DEFAULT_AGENT."""
        result = main(agent=None)
        assert result == 0

    def test_main_uses_default_agent(self):
        """Test that default agent is used when none specified."""
        with patch("nchantrs.cli.logger") as mock_logger:
            main()
            # Check that info was logged
            assert mock_logger.info.called


class TestCommandFunctions:
    """Tests for individual command functions."""

    def test_cmd_run(self):
        """Test run command returns 0."""
        result = cmd_run([])
        assert result == 0

    def test_cmd_run_with_agent(self):
        """Test run command with custom agent."""
        result = cmd_run([], agent="test_agent")
        assert result == 0

    def test_cmd_test(self):
        """Test test command returns 0."""
        result = cmd_test([])
        assert result == 0

    def test_cmd_install(self):
        """Test install command returns 0."""
        result = cmd_install([])
        assert result == 0

    def test_cmd_uninstall(self):
        """Test uninstall command returns 0."""
        result = cmd_uninstall([])
        assert result == 0

    def test_cmd_config(self):
        """Test config command returns 0."""
        result = cmd_config([])
        assert result == 0

    def test_cmd_version(self):
        """Test version command returns 0."""
        result = cmd_version([])
        assert result == 0

    def test_cmd_help(self):
        """Test help command returns 0."""
        result = cmd_help([])
        assert result == 0

    def test_cmd_actions(self):
        """Test actions command returns 0."""
        result = cmd_actions([])
        assert result == 0

    def test_cmd_dialogs(self):
        """Test dialogs command returns 0."""
        result = cmd_dialogs([])
        assert result == 0

    def test_cmd_events(self):
        """Test events command returns 0."""
        result = cmd_events([])
        assert result == 0

    def test_cmd_models(self):
        """Test models command returns 0."""
        result = cmd_models([])
        assert result == 0

    def test_cmd_services(self):
        """Test services command returns 0."""
        result = cmd_services([])
        assert result == 0

    def test_cmd_utilities(self):
        """Test utilities command returns 0."""
        result = cmd_utilities([])
        assert result == 0

    def test_cmd_widgets(self):
        """Test widgets command returns 0."""
        result = cmd_widgets([])
        assert result == 0

    def test_cmd_wizards(self):
        """Test wizards command returns 0."""
        result = cmd_wizards([])
        assert result == 0

    def test_cmd_extensions(self):
        """Test extensions command returns 0."""
        result = cmd_extensions([])
        assert result == 0

    def test_cmd_libraries(self):
        """Test libraries command returns 0."""
        result = cmd_libraries([])
        assert result == 0

    def test_cmd_library(self):
        """Test library command returns 0."""
        result = cmd_library([])
        assert result == 0

    def test_cmd_logging_module(self):
        """Test logging command returns 0."""
        result = cmd_logging([])
        assert result == 0

    def test_cmd_themes(self):
        """Test themes command returns 0."""
        result = cmd_themes([])
        assert result == 0

    def test_cmd_updates(self):
        """Test updates command returns 0."""
        result = cmd_updates([])
        assert result == 0

    def test_cmd_views(self):
        """Test views command returns 0."""
        result = cmd_views([])
        assert result == 0


class TestDefaultConstants:
    """Tests for default constants."""

    def test_default_agent_value(self):
        """Test DEFAULT_AGENT is 'arthr'."""
        assert DEFAULT_AGENT == "arthr"

    def test_default_agent_name_value(self):
        """Test DEFAULT_AGENT_NAME is 'arthr'."""
        assert DEFAULT_AGENT_NAME == "arthr"
