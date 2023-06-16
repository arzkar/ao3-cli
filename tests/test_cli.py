from click.testing import CliRunner
from ao3_cli.cli import run_cli


def test_cli_url(tmpdir):
    runner = CliRunner()

    with runner.isolated_filesystem():
        result = runner.invoke(run_cli, [
            '-u https://archiveofourown.org/works/31950595'])

    assert not result.exception
    assert result.exit_code == 0


def test_cli_list_url():
    runner = CliRunner()

    with runner.isolated_filesystem():
        result = runner.invoke(run_cli, [
            "-l", "https://archiveofourown.org/works/31923052/chapters/79053661,https://archiveofourown.org/works/31950595"])

    assert not result.exception
    assert result.exit_code == 0


def test_cli_infile():
    runner = CliRunner()

    with runner.isolated_filesystem():

        # create urls.txt with sample urls
        with open('urls.txt', 'w') as f:
            f.write(
                'https://archiveofourown.org/works/30820292\nhttps://archiveofourown.org/works/25715935/chapters/62441215')

        result = runner.invoke(run_cli, [
            "-i", "urls.txt"])

    assert not result.exception
    assert result.exit_code == 0


def test_cli_version():
    runner = CliRunner()

    result = runner.invoke(run_cli, ['-v'])

    assert not result.exception
    assert result.exit_code == 0
    assert result.output.strip() == 'Version: 0.1.6'
