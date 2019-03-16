import nibabel, tempfile, os, numpy as np, sys
from ctypes import c_char, sizeof, c_wchar_p, create_string_buffer
from geometry_core import geometry_core

def nii2mesh(file):
    stack = nibabel.load(file)
    header = stack.header
    a = np.array(stack.dataobj)

    x_dim = a.shape[0]
    y_dim = a.shape[1]
    z_dim = a.shape[2]

    voxel_size_x = header.get_zooms()[0]
    voxel_size_y = header.get_zooms()[1]
    voxel_size_z = header.get_zooms()[2]

    header_attrs = {'XDIM': x_dim, 'YDIM': y_dim, 'ZDIM': z_dim, 'VDIM': 1,
        'TYPE': 'unsigned fixed', 'PIXSIZE': '8 bits', 'CPU': 'decm', 'VX': voxel_size_x,
        'VY': voxel_size_y, 'VZ': voxel_size_z}

    inr_header = '#INRIMAGE-4#{\n'

    inr_header += '\n'.join([f'{key}={value}' for key, value in header_attrs.items()])
    header_end = '##}\n'

    hlen = 256 - len(inr_header + header_end)

    inr_header += ''.join(['\n' for i in range(hlen)]) + header_end

    inr_header = inr_header

    data = [c_char(int(a[i,j,k])) for i in range(x_dim) for j in range(y_dim) for k in range(z_dim)]

    c_str = create_string_buffer(bytes(inr_header, 'utf-8'))

    fd, path = tempfile.mkstemp()

    try:
        with os.fdopen(fd, 'wb') as tmp:
            tmp.write(c_str.raw)
            for char in data:
                tmp.write(char)
    finally:
        os.remove(path)
