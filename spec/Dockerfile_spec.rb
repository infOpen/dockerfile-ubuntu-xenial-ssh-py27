require 'docker'
require 'infopen-docker'
require 'serverspec'

describe 'Dockerfile' do

    # Build Dockerfile
    before(:all) do
        @image = Docker::Image.build_from_dir('.')

        set :os, family: :debian
        set :backend, :docker
        set :docker_image, @image.id
    end

    # Once tests done, remove image
    after(:all) do
        Infopen::Docker::Lifecycle.remove_image_and_its_containers(@image)
    end


    # Tests
    #------

    it 'installs the right version of Ubuntu' do
        expect(get_os_version()).to include('Ubuntu 16.04')
    end

    it 'installs ssh server package' do
        expect(package('openssh-server')).to be_installed
    end

    it 'runs ssh server service' do
        expect(service('sshd')).to be_running
        expect(process('sshd')).to be_running
        expect(port(22)).to be_listening.with('tcp')
    end

    it 'installs Python 2.7 packages' do
        expect(package('python2.7')).to be_installed
        expect(package('python2.7-dev')).to be_installed
    end


    # Functions
    #----------

    # Get os version of container
    def get_os_version
        command('lsb_release -a').stdout
    end
end

