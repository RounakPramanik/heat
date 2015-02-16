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

from heat.openstack.common.gettextutils import _
from heat.engine import clients
from heat.engine import constraints
from heat.engine import properties
from heat.engine.resources.vnfsvc import vnfsvc
from heat.openstack.common import log as logging


logger = logging.getLogger(__name__)
SERVICE_TYPES = "firewall"

class Service(vnfsvc.VNFSvcResource):
    """
    A resource for the Service Name resource in VNFsvc .
    """

    PROPERTIES = (
        NAME,DESCRIPTION,QUALITY_OF_SERVICE,ATTRIBUTES,
    ) = (
        'name', 'description','quality_of_service', 'attributes'
    )

    properties_schema = {
        NAME: properties.Schema(
            properties.Schema.STRING,
            _('Service name to create the cluster'),
            required=True,
            update_allowed=True
        ),
        DESCRIPTION: properties.Schema(
            properties.Schema.STRING,
            _('Description of the service'),
            required=True,
            update_allowed=True
        ),
        QUALITY_OF_SERVICE: properties.Schema(
            properties.Schema.STRING,
            _('quality of service'),
            required=True,
            update_allowed=True
        ),
        ATTRIBUTES: properties.Schema(
            properties.Schema.MAP,
            _('attributes'),
            required=True,
            update_allowed=True
        )


    }

    attributes_schema = {
        'name': _('Name of service'),
        'description': _('Description of the service'),
        'quality_of_service': _('quality of service'),
        'attributes': _('attributes'),
    }

    update_allowed_keys = ('Properties',)

    def _show_resource(self):
         device = self.vnfsvc().show_vnf(self.resource_id)['service']
         if device == {}:
            return

    def handle_create(self):
        service_props={}
        props = self.prepare_properties(
            self.properties,
            self.physical_resource_name())
        service_props['name']=props['name']
        service_props['description']=props['description']
        service_props['quality_of_service']=props['quality_of_service']
        service_props['attributes'] = props['attributes']
        service = self.vnfsvc().create_service({'service': service_props})['service']
        self.resource_id_set(service['id'])

    def handle_update(self, json_snippet, tmpl_diff, prop_diff):
        if prop_diff:
            self.vnfsvc().update_service(
                self.resource_id, {'service': prop_diff})

    def handle_delete(self):
        client = self.vnfsvc()
        try:
            client.delete_service(self.resource_id)
            return
        except Exception as ex:
            self.client_plugin().ignore_not_found(ex)


class VNF(vnfsvc.VNFSvcResource):
    """
    A resource for the VNF resource in VNFsvc .
    """

    PROPERTIES = (
        TEMPLATE_ID,SERVICE_CONTEXTS,USERNAME,PASSWORD,GROUP_ID,
    ) = (
        'template_id', 'service_contexts','username','password','group_id'
    )

    properties_schema = {
        TEMPLATE_ID: properties.Schema(
            properties.Schema.STRING,
            _('vnf template id to create vnf based on.'),
            required=True,
            update_allowed=True
        ),
        USERNAME: properties.Schema(
            properties.Schema.STRING,
            _('username to create vnf based on.'),
            required=True,
            update_allowed=True
        ),
        PASSWORD: properties.Schema(
            properties.Schema.STRING,
            _('password to create vnf based on.'),
            required=True,
            update_allowed=True
        ),
        SERVICE_CONTEXTS: properties.Schema(
            properties.Schema.LIST,
            _('service context to insert service.'),
            update_allowed=True
        ),
        GROUP_ID: properties.Schema(
            properties.Schema.STRING,
            _('group id for a vnf group'),
            required=False,
            update_allowed=True
        ),


    }

    attributes_schema = {
        'template_id': _('vnf template id to create vnf based on.'),
        'service_contexts': _('service context to insert service.'),
        'username':_('username to create vnf based on.'),
        'password':_('password to create vnf based on.'),
        'group_id':_('group id for a vnf group.'),
    }

    update_allowed_keys = ('Properties',)

    def _show_resource(self):
         device = self.vnfsvc().show_vnf(self.resource_id)['vnf']
         if device == {}:
            return

    def handle_create(self):
        vnf_props={}
        props = self.prepare_properties(
            self.properties,
            self.physical_resource_name())
        vnf_props['template_id']=props['template_id']
        vnf_props['username']=props['username']
        vnf_props['password']=props['password']
        vnf_props['service_contexts']=props['service_contexts']
        vnf_props['group_id']=props['group_id']
        vnf = self.vnfsvc().create_vnf({'vnf': vnf_props})['vnf']        
        if 'device' in vnf.keys():
            self.resource_id_set(vnf['device']['id'])
        else:
            self.resource_id_set(vnf['id'])

    def handle_update(self, json_snippet, tmpl_diff, prop_diff):
        if prop_diff:
            self.vnfsvc().update_vnf(
                self.resource_id, {'vnf': prop_diff})

    def handle_delete(self):
        client = self.vnfsvc()
        try:
            client.delete_vnf(self.resource_id)
        except Exception as ex:
            self.client_plugin().ignore_not_found(ex)
        else:
            return self._delete_task()

class VNFTemplate(vnfsvc.VNFSvcResource):
    """
    A resource for the VNFTemplate resource in VNFsvc .
    """

    PROPERTIES = (
        NAME, DESCRIPTION, SERVICE_TYPE, MGMT_DRIVER,
        ATTRIBUTES,
    ) = (
        'name', 'description', 'service_type',
        'mgmt_driver', 'attributes',
    )

    properties_schema = {
        NAME: properties.Schema(
            properties.Schema.STRING,
            _('Name for the vnf template.'),
            update_allowed=True
        ),
        DESCRIPTION: properties.Schema(
            properties.Schema.STRING,
            _('Description for the vnf template.'),
            update_allowed=True
        ),
        SERVICE_TYPE: properties.Schema(
            properties.Schema.STRING,
            _('service type for the vnf template .'),
            update_allowed=True
        ),
        MGMT_DRIVER: properties.Schema(
            properties.Schema.STRING,
            _('manegement driver name for the vnftemplate.'),
            update_allowed=True
        ),
        ATTRIBUTES: properties.Schema(
            properties.Schema.MAP,
            _('set servicetypes for the vnftemplate'),
            update_allowed=True
        ),

    }

    attributes_schema = {
        'name': _('Name for the vnf template.'), 
        'description': _('Description of the vnf template.'),
        'service_type': _('service type for vnf template.'),
        'mgmt_driver': _('management driver for this vnf template.'),
        'attribute': _('service types for vnf template.'),
    }

    update_allowed_keys = ('Properties',)

    def _show_resource(self):
         pass
    #    return self.vnfsvc().show_vnf_template(
    #        self.resource_id)['vnf_template']

    def handle_create(self):
        props = self.prepare_properties(
            self.properties,
            self.physical_resource_name())
        vnf_template_props = {}
        vnf_template_props['name'] = props['name']
        vnf_template_props['description'] = props['description']
        vnf_template_props['mgmt_driver'] = props['mgmt_driver']
        vnf_template_props['service_type'] = props['service_type']
        vnf_template_props['attributes'] = props['attributes']
        vnf_template = self.vnfsvc().create_vnf_template(
            {'vnf_template': vnf_template_props})['vnf_template']
        if  props['service_type'] not in SERVICE_TYPES:
            self.resource_id_set(vnf_template['id'])
        elif props['service_type'] in ['router','loadbalancer']:
            pass
        else:
            self.resource_id_set(vnf_template['device_template']['id'])

    def handle_update(self, json_snippet, tmpl_diff, prop_diff):
        if prop_diff:
            self.vnfsvc().update_vnf_template(
                self.resource_id, {'vnf_template': prop_diff})

    def handle_delete(self):
        client = self.vnfsvc()
        try:
            client.delete_vnf_template(self.resource_id)
        except Exception as ex:
            self.client_plugin().ignore_not_found(ex)
        else:
            return self._delete_task()


def resource_mapping():
    return {
        'OS::VNFSvc::VNF': VNF,
        'OS::VNFSvc::VNFTemplate': VNFTemplate,
        'OS::VNFSvc::Service': Service,
    }
        
