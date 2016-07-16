import pytest
import testinfra

# Use testinfra to get a handy function to run commands locally
check_output = testinfra.get_backend(
    "local://"
).get_module("Command").check_output


@pytest.fixture
def TestinfraBackend(request):
    # Override the TestinfraBackend fixture,
    # all testinfra fixtures (i.e. modules) depend on it.

    docker_image = request.param

    # Check if a Docker image testing
    if request.param == 'build:current_folder':
        docker_image = check_output(
            'docker build .').split('\n')[-1].split(' ')[-1]

    docker_id = check_output(
        "docker run --privileged -v /sys/fs/cgroup:/sys/fs/cgroup:ro -d -P %s",
        docker_image
    )

    def teardown():
        check_output("docker rm -f %s", docker_id)

        # If Docker image testing, remove image after tests
        if request.param == 'build:current_folder':
            check_output("docker rmi -f %s", docker_image)

    # Destroy the container at the end of the fixture life
    request.addfinalizer(teardown)

    # Return a dynamic created backend
    return testinfra.get_backend("docker://" + docker_id)


def pytest_generate_tests(metafunc):
    if "TestinfraBackend" in metafunc.fixturenames:

        # Lookup "docker_images" marker
        marker = getattr(metafunc.function, "docker_images", None)
        if marker is not None:
            images = marker.args
        else:
            # Default image
            images = ["debian:jessie"]

        # If the test has a destructive marker, we scope TestinfraBackend
        # at function level (i.e. executing for each test). If not we scope
        # at session level (i.e. all tests will share the same container)
        if getattr(metafunc.function, "destructive", None) is not None:
            scope = "function"
        else:
            scope = "session"

        metafunc.parametrize(
            "TestinfraBackend", images, indirect=True, scope=scope)
