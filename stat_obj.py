import pywavefront

orignal_vertices = "/home/kj/Data/me/OUT_PRNET/t1head_o.obj"
clean_vertices = "/home/kj/Data/me/OUT_PRNET/t1head_wo_ear.obj"

oscene = pywavefront.Wavefront(orignal_vertices, strict=True, parse=False)
nscene = pywavefront.Wavefront(clean_vertices, strict=True, parse=False)

oscene.parse()
nscene.parse()

all_vert = []

i=0
for name, material in oscene.materials.items():
    # all_vert.append(material.vertices)
    print("# material.vertices: ", material.vertices)
    print("# i: ", i)