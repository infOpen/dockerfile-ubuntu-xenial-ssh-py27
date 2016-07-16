import pytest


pytestmark = pytest.mark.docker_images('build:current_folder')


def test_system_version(SystemInfo):
    """
    Check image system version
    """

    assert SystemInfo.codename == 'xenial'


def test_packages(Package):
    """
    Check installed packages
    """

    packages = ['openssh-server', 'python2.7', 'python2.7-dev']

    for package in packages:
        assert Package(package).is_installed


def test_sshd(Command, Process, Service, Socket):
    """
    Check SSH service state
    """

    assert Service('ssh').is_enabled
    assert Service('ssh').is_running
    assert Command('systemctl status sshd').rc == 0
    assert len(Process.filter(comm='sshd')) == 1
    assert Socket("tcp://0.0.0.0:22").is_listening
