# Copyright 2015 NEC Corporation.  All rights reserved.
#
#    Licensed under the Apache License, Version 2.0 (the "License"); you may
#    not use this file except in compliance with the License. You may obtain
#    a copy of the License at
#
#         http://www.apache.org/licenses/LICENSE-2.0
#
#    Unless required by applicable law or agreed to in writing, software
#    distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
#    WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
#    License for the specific language governing permissions and limitations
#    under the License.

from magnumclient.common import cliutils as utils
from magnumclient.common import utils as magnum_utils
from magnumclient.i18n import _


# Maps old parameter names to their new names and whether they are required
DEPRECATING_PARAMS = {
    "--external-network-id": "--external-network",
    "--flavor-id": "--flavor",
    "--image-id": "--image",
    "--keypair-id": "--keypair",
    "--master-flavor-id": "--master-flavor",
}


def _show_cluster_template(cluster_template):
    del cluster_template._info['links']
    utils.print_dict(cluster_template._info)


@utils.deprecation_map(DEPRECATING_PARAMS)
@utils.arg('--name',
           metavar='<name>',
           help='Name of the cluster template to create.')
@utils.arg('--image-id',
           dest='image',
           required=True,
           metavar='<image>',
           help=utils.deprecation_message(
               'The name or UUID of the base image to customize for the '
               'Cluster.', 'image'))
@utils.arg('--image',
           dest='image',
           required=True,
           metavar='<image>',
           help='The name or UUID of the base image to customize for the '
                'Cluster.')
@utils.arg('--keypair-id',
           dest='keypair',
           metavar='<keypair>',
           help=utils.deprecation_message(
               'The name or UUID of the SSH keypair to load into the '
               'Cluster nodes.', 'keypair'))
@utils.arg('--keypair',
           dest='keypair',
           metavar='<keypair>',
           help='The name or UUID of the SSH keypair to load into the Cluster '
                'nodes.')
@utils.arg('--external-network-id',
           dest='external_network',
           required=True,
           metavar='<external-network>',
           help=utils.deprecation_message(
                'The external Neutron network name or UUID to connect to '
                'this Cluster Template.', 'external-network'))
@utils.arg('--external-network',
           dest='external_network',
           required=True,
           metavar='<external-network>',
           help='The external Neutron network name or UUID to connect to '
                'this Cluster Template.')
@utils.arg('--coe',
           required=True,
           metavar='<coe>',
           help='Specify the Container Orchestration Engine to use.')
@utils.arg('--fixed-network',
           metavar='<fixed-network>',
           help='The private Neutron network name to connect to this Cluster'
           ' model.')
@utils.arg('--fixed-subnet',
           metavar='<fixed-subnet>',
           help='The private Neutron subnet name to connect to Cluster.')
@utils.arg('--network-driver',
           metavar='<network-driver>',
           help='The network driver name for instantiating container'
           ' networks.')
@utils.arg('--volume-driver',
           metavar='<volume-driver>',
           help='The volume driver name for instantiating container'
           ' volume.')
@utils.arg('--dns-nameserver',
           metavar='<dns-nameserver>',
           default='8.8.8.8',
           help='The DNS nameserver to use for this cluster template.')
@utils.arg('--flavor-id',
           dest='flavor',
           metavar='<flavor>',
           default='m1.medium',
           help=utils.deprecation_message(
                'The nova flavor name or UUID to use when launching the '
                'Cluster.', 'flavor'))
@utils.arg('--flavor',
           dest='flavor',
           metavar='<flavor>',
           default='m1.medium',
           help='The nova flavor name or UUID to use when launching the '
                'Cluster.')
@utils.arg('--master-flavor-id',
           dest='master_flavor',
           metavar='<master-flavor>',
           help=utils.deprecation_message(
                'The nova flavor name or UUID to use when launching the master'
                ' node of the Cluster.', 'master-flavor'))
@utils.arg('--master-flavor',
           dest='master_flavor',
           metavar='<master-flavor>',
           help='The nova flavor name or UUID to use when launching the master'
                ' node of the Cluster.')
@utils.arg('--docker-volume-size',
           metavar='<docker-volume-size>',
           type=int,
           help='Specify the number of size in GB '
                'for the docker volume to use.')
@utils.arg('--docker-storage-driver',
           metavar='<docker-storage-driver>',
           default='devicemapper',
           help='Select a docker storage driver. Supported: devicemapper, '
                'overlay. Default: devicemapper')
@utils.arg('--http-proxy',
           metavar='<http-proxy>',
           help='The http_proxy address to use for nodes in Cluster.')
@utils.arg('--https-proxy',
           metavar='<https-proxy>',
           help='The https_proxy address to use for nodes in Cluster.')
@utils.arg('--no-proxy',
           metavar='<no-proxy>',
           help='The no_proxy address to use for nodes in Cluster.')
@utils.arg('--labels', metavar='<KEY1=VALUE1,KEY2=VALUE2;KEY3=VALUE3...>',
           action='append', default=[],
           help='Arbitrary labels in the form of key=value pairs '
                'to associate with a cluster template. '
                'May be used multiple times.')
@utils.arg('--tls-disabled',
           action='store_true', default=False,
           help='Disable TLS in the Cluster.')
@utils.arg('--public',
           action='store_true', default=False,
           help='Make cluster template public.')
@utils.arg('--registry-enabled',
           action='store_true', default=False,
           help='Enable docker registry in the Cluster')
@utils.arg('--server-type',
           metavar='<server-type>',
           default='vm',
           help='Specify the server type to be used '
                'for example vm. For this release '
                'default server type will be vm.')
@utils.arg('--master-lb-enabled',
           action='store_true', default=False,
           help='Indicates whether created Clusters should have a load '
                'balancer for master nodes or not.')
@utils.arg('--floating-ip-enabled',
           action='store_true', default=True,
           help='Indicates whether created Clusters should have a floating ip'
                'or not.')
@utils.arg('--monitoring-enabled',
           action='store_true', default=False,
           help='Indicates whether to setup the container based monitoring stack'
                'or not.')
def do_cluster_template_create(cs, args):
    """Create a cluster template."""
    opts = {}
    opts['name'] = args.name
    opts['flavor_id'] = args.flavor
    opts['master_flavor_id'] = args.master_flavor
    opts['image_id'] = args.image
    opts['keypair_id'] = args.keypair
    opts['external_network_id'] = args.external_network
    opts['fixed_network'] = args.fixed_network
    opts['fixed_subnet'] = args.fixed_subnet
    opts['network_driver'] = args.network_driver
    opts['volume_driver'] = args.volume_driver
    opts['dns_nameserver'] = args.dns_nameserver
    opts['docker_volume_size'] = args.docker_volume_size
    opts['docker_storage_driver'] = args.docker_storage_driver
    opts['coe'] = args.coe
    opts['http_proxy'] = args.http_proxy
    opts['https_proxy'] = args.https_proxy
    opts['no_proxy'] = args.no_proxy
    opts['labels'] = magnum_utils.handle_labels(args.labels)
    opts['tls_disabled'] = args.tls_disabled
    opts['public'] = args.public
    opts['registry_enabled'] = args.registry_enabled
    opts['server_type'] = args.server_type
    opts['master_lb_enabled'] = args.master_lb_enabled
    opts['floating_ip_enabled'] = args.floating_ip_enabled
    opts['monitoring_enabled'] = args.monitoring_enabled

    cluster_template = cs.cluster_templates.create(**opts)
    _show_cluster_template(cluster_template)


@utils.arg('cluster_templates',
           metavar='<cluster_templates>',
           nargs='+',
           help='ID or name of the (cluster template)s to delete.')
def do_cluster_template_delete(cs, args):
    """Delete specified cluster template."""
    for cluster_template in args.cluster_templates:
        try:
            cs.cluster_templates.delete(cluster_template)
            print("Request to delete cluster template %s has been accepted." %
                  cluster_template)
        except Exception as e:
            print("Delete for cluster template "
                  "%(cluster_template)s failed: %(e)s" %
                  {'cluster_template': cluster_template, 'e': e})


@utils.arg('cluster_template',
           metavar='<cluster_template>',
           help='ID or name of the cluster template to show.')
def do_cluster_template_show(cs, args):
    """Show details about the given cluster template."""
    cluster_template = cs.cluster_templates.get(args.cluster_template)
    _show_cluster_template(cluster_template)


@utils.arg('--limit',
           metavar='<limit>',
           type=int,
           help='Maximum number of cluster templates to return')
@utils.arg('--sort-key',
           metavar='<sort-key>',
           help='Column to sort results by')
@utils.arg('--sort-dir',
           metavar='<sort-dir>',
           choices=['desc', 'asc'],
           help='Direction to sort. "asc" or "desc".')
@utils.arg('--fields',
           default=None,
           metavar='<fields>',
           help=_('Comma-separated list of fields to display. '
                  'Available fields: uuid, name, coe, image_id, public, link, '
                  'apiserver_port, server_type, tls_disabled, registry_enabled'
                  )
           )
def do_cluster_template_list(cs, args):
    """Print a list of cluster templates."""
    nodes = cs.cluster_templates.list(limit=args.limit,
                                      sort_key=args.sort_key,
                                      sort_dir=args.sort_dir)
    columns = ['uuid', 'name']
    columns += utils._get_list_table_columns_and_formatters(
        args.fields, nodes,
        exclude_fields=(c.lower() for c in columns))[0]
    utils.print_list(nodes, columns,
                     {'versions': magnum_utils.print_list_field('versions')},
                     sortby_index=None)


@utils.arg('cluster_template',
           metavar='<cluster_template>',
           help="UUID or name of cluster template")
@utils.arg(
    'op',
    metavar='<op>',
    choices=['add', 'replace', 'remove'],
    help="Operations: 'add', 'replace' or 'remove'")
@utils.arg(
    'attributes',
    metavar='<path=value>',
    nargs='+',
    action='append',
    default=[],
    help="Attributes to add/replace or remove "
         "(only PATH is necessary on remove)")
def do_cluster_template_update(cs, args):
    """Updates one or more cluster template attributes."""
    patch = magnum_utils.args_array_to_patch(args.op, args.attributes[0])

    cluster_template = cs.cluster_templates.update(args.cluster_template,
                                                   patch)
    _show_cluster_template(cluster_template)
