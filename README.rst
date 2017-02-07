Misc ansible pieces to help with various ops tasks

Working with ``supervisord`` agents
===================================

There are 2 ansible playbooks for supervisord operations:
    - supervisord-action.yml
    - supervisord-status.yml

Both operate on all hosts provided in the inventory. The inventory must
also provide variable ``service_list`` for the services to be managed.

For supervisord-action.yml, a ``desired_state`` must be provided from a
legal value from `ansible 1.9 supervisorctl`_ module.

Example::

    ansible-playbook -i selfserve-inventory.sh supervisord-action.yml \
        -e desired_state=stopped

.. _ansible 1.9 supervisorctl: http://docs.ansible.com/ansible/supervisorctl_module.html
