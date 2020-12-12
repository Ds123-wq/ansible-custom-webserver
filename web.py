- hosts: all
  vars_files:
    - vars.py
  tasks:
  - name: "create mountpoint"
    file:
      path: "{{ mount_point }}"
      state: directory
  - name: "mount the dvd"
    mount:
      path: "{{ mount_point }}"
      src: "/dev/cdrom"
      state: mounted
      fstype: "iso9660"
  - name: "configure yum"
    yum_repository:
      name: "AppStream"
      description: "configure AppStream"
      baseurl: "{{ mount_point }}/AppStream"
      gpgcheck: no
  - name: "configure yum"
    yum_repository:
      name: "BaseOS"
      description: "configure BaseOS"
      baseurl: "{{ mount_point }}/BaseOS"
      gpgcheck: no

  - name: "Install httpd"
    package:
      name: "httpd"
  - name: "create document_root"

    file:
      path: "{{ document_root }}"
      state: directory
  - name: "copy the webpage"
    copy:
      dest: "{{ document_root }}/index.html"
      src: "webpage.html"

  - name: "copy the conf file"
    template:
      src: "lw.conf.j2"
      dest: "/etc/httpd/conf.d/lw.conf"
    notify: Restart service


  - name: "create firewall rule"
    firewalld:
      port: "{{ http_port }}/tcp"
      immediate: yes
      state: enabled

  handlers:
  - name: "Restart service"
    service:
      name: "httpd"
      state: restarted
      enabled: yes

