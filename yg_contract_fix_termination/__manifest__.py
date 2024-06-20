# Copyright 2024 Yves Goldberg (Ygol InternetWork)
# Part of module yg_contract_fix_termination. See LICENSE file for
# full copyright and licensing details.

{
    'name': 'Yg Contract Fix Termination',
    'description': """
        Fix termination bug""",
    'version': '16.0.1.0.1',
    'license': 'Other proprietary',
    'author': 'Yves Goldberg (Ygol InternetWork)',
    'website': 'https://www.ygol.com',
    'depends': [
        'contract'
    ],
    'external_dependencies': {"python": [], "bin": []},
    'data': [
        "views/contract.xml",
    ],
    'demo': [
    ],
    'qweb': [
    ],
    'post_load': None,
    'pre_init_hook': None,
    'post_init_hook': None,
    'uninstall_hook': None,

    'auto_install': False,
    'installable': True,
    'application': True,
}
