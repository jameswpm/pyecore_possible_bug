from os import path as osp
from pathlib import Path

#PyEcore
from pyecore.resources import ResourceSet, URI, AbstractURIConverter

class FileSpecificProtocolURIConverter(AbstractURIConverter):
    @staticmethod
    def can_handle(uri):
        return uri.protocol == 'file'

    @staticmethod
    def convert(uri):
        return URI(osp.abspath(uri.plain.replace('file:/', '')))

RESOURCES_PATH = osp.join(Path(__file__).parent)

ecore_path = osp.join(RESOURCES_PATH, '..', 'A.ecore')
xmi_path = osp.join(RESOURCES_PATH, '..', 'BaseClass.xmi')

resource_set = ResourceSet()
resource_set.uri_converter.append(FileSpecificProtocolURIConverter)
#register metamodel
resource_path = resource_set.get_resource(URI(ecore_path))
content = resource_path.contents[0]
resource_set.metamodel_registry[content.nsURI] = content
#register model
m_resource = resource_set.get_resource(URI(xmi_path))


#iterate the model and print the class name
for element in m_resource.contents:    
    class_name = element.eClass.name
    print(f'Class {class_name} with attribute {element.eGet("simpleAttr")}')                  
    object_element = element.object
    object_element_class = object_element.eClass.name
    print(f'Reference Class {object_element_class} with attribute {object_element.eGet("simpleAttr")}')
