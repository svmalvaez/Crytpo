from django.shortcuts import render, render_to_response, redirect
from django.template import RequestContext
from django.views.generic.base import View
from django.http import HttpResponse, StreamingHttpResponse, Http404
from . import OperationModes as op
from .HillCipher import HillCipher as hc
from .Tools import mod, file_format, get_colors, save_image, create_zip
from zipfile import ZipFile
import tempfile
import json, os

KEY = [[1,2,3],[4,5,6],[11,9,8]]
KEY_INVERSE = [[90,167,1],[74,179,254],[177,81,1]]


def modes_operation_encrypt(request):
    res = {
        'status': False,
        'current_progress': 0,
        'errors': False,
        'status_txt': 'No has seleccionado una imagen',
        'total_imgs': 0,
    }
    def __process_encrypt():
        
        paths = []
        hill_instance = hc(key=KEY, ikey= KEY_INVERSE)
        init_vector = [133,10,39]
        ecb = op.ECB(cipher_instance = hill_instance)
        cbc = op.CBC(cipher_instance = hill_instance, init_vector=init_vector)
        cfb = op.CFB(cipher_instance = hill_instance, init_vector=init_vector)
        ofb = op.OFB(cipher_instance = hill_instance, init_vector=init_vector)
        ctr = op.CTR(cipher_instance = hill_instance, init_vector=init_vector)

        res = {
            'status': False,
            'current_progress': 0,
            'errors': False,
            'status_txt': 'Processing...',
            'total_imgs': 0,
            'zip_id': None
        }

        
        _file = request.FILES['original_img']
        ext = file_format(_file)
        colors, size = get_colors(_file)
        e_colors = []

        response = json.dumps(res)
        yield 'JSON!_!SEP' + str(response)

        for it in range(0,6):
            res['total_imgs'] += 1
            res['status_txt'] = 'Encrypted with: %d of %d ciphers' % (res['total_imgs'], 5)
            if it is 0:
                """ 1 >>> ECB """
                for i,color in enumerate(colors):
                    e_colors.append(ecb.encrypt(p=color))            

                for i, color in enumerate(e_colors):
                    e_colors[i] = mod(color, 256)

                ecb_path = save_image(e_colors, size)        
                paths.append(ecb_path)

                #yield json.dumps(res)

            elif it is 1:
                """ 2 >>> CBC """
                e_colors = []
                for i, color in enumerate(colors):
                    e_colors.append(cbc.encrypt(p=color))

                for i, color in enumerate(e_colors):
                    e_colors[i] = mod(color, 256)

                cbc_path = save_image(e_colors, size)
                paths.append(cbc_path)

            elif it is 2:
                """ 3 >>> CFB """
                e_colors = []
                for i, color in enumerate(colors):
                    e_colors.append(cfb.encrypt(p=color))

                for i, color in enumerate(e_colors):
                    e_colors[i] = mod(color, 256)

                cfb_path = save_image(e_colors, size)
                paths.append(cfb_path)

            elif it is 3:
                """ 4 >>> OFB """
                e_colors = []
                for i, color in enumerate(colors):
                    e_colors.append(ofb.encrypt(p=color))

                for i, color in enumerate(e_colors):
                    e_colors[i] = mod(color, 256)

                ofb_path = save_image(e_colors, size)
                paths.append(ofb_path)

            elif it is 4:
                """ 5 >>> CTR """
                e_colors = []
                for i, color in enumerate(colors):
                    e_colors.append(ctr.encrypt(p=color))

                for i, color in enumerate(e_colors):
                    e_colors[i] = mod(color, 256)

                ctr_path = save_image(e_colors, size)
                paths.append(ctr_path)

            elif it is 5:
                """ >>> CREATE ZIPFILE """
                zip_path = create_zip(paths, _file.name.split('.')[0], ext)
                res['zip_id'] = zip_path.split('/')[-1].split('.zip')[0]
                res['total_imgs'] -= 1
                res['status_txt'] = 'Completed!! :) [%s]' % res['zip_id']
            
            response = json.dumps(res)
            yield 'JSON!_!SEP' + str(response)


    if 'original_img' in request.FILES:
        return StreamingHttpResponse(__process_encrypt())
    else:
        return HttpResponse(json.dumps(res), content_type='plain/text')

def modes_operation_decrypt(request):
    """-"""
    res = {
        'status': False,
        'current_progress': 0,
        'errors': False,
        'status_txt': 'No has seleccionado una imagen o un cifrador',
        'total_imgs': 0,
    }

    def __process_decrypt():
        hill_instance = hc(key=KEY, ikey= KEY_INVERSE)
        init_vector = [133,10,39]
        op_mode = (request.POST['decryption_mode']).lower()
       
        _file = request.FILES['original_img']
        ext = file_format(_file)
        colors, size = get_colors(_file)
        e_colors = []
        total_colors = len(colors)

        print op_mode
        opmode = op.ECB(cipher_instance = hill_instance)
        if op_mode == 'ecb':
            pass
        elif op_mode == 'cbc':
            opmode = op.CBC(cipher_instance = hill_instance, init_vector=init_vector)
        elif op_mode == 'cfb':
            opmode = op.CFB(cipher_instance = hill_instance, init_vector=init_vector)
        elif op_mode == 'ofb':
            opmode = op.OFB(cipher_instance = hill_instance, init_vector=init_vector)
        elif op_mode == 'ctr':
            opmode = op.CTR(cipher_instance = hill_instance, init_vector=init_vector)

        res = {
            'status': False,
            'current_progress': 0,
            'errors': False,
            'status_txt': 'Decryption process 0%...',
            'total_imgs': 0,
            'zip_id': None
        }

        response = json.dumps(res)
        yield 'JSON!_!SEP' + str(response)
        
        prev = 0
        for i, color in enumerate(colors):
            e_colors.append(opmode.decrypt(c=color))
            percentage = int(i * 100 / total_colors)
            if percentage > prev:
                prev = percentage
                res['status_txt'] = 'Decryption process %.2f ...' % percentage
                response = json.dumps(res)
                yield 'JSON!_!SEP' + str(response)
   
        for i, color in enumerate(e_colors):
            e_colors[i] = mod(color, 256)

        img_path = save_image(e_colors, size)        
        res['zip_id'] = img_path.split('/')[-1]
        res['status_txt'] = 'Completed!!...'
        response = json.dumps(res)
        yield 'JSON!_!SEP' + str(response)


    if 'original_img' in request.FILES and 'decryption_mode' in request.POST:
        return StreamingHttpResponse(__process_decrypt())
    else:
        return HttpResponse(json.dumps(res), content_type='plain/text')

def get_zip(request, temp_zip):
    zip_path = "/tmp/%s.zip" % temp_zip
    try:
        zip_file = open(zip_path)
    except:
        raise Http404
    fw = FileWrapper(zip_file)
    os.remove(zip_path)
    response = HttpResponse(fw, content_type='application/zip')
    response['Content-Disposition'] = 'attachment; filename="%s_encrypted.zip"' %  temp_zip

    return response
    

def get_img(request, temp_img):
    img_path = "/tmp/%s" % temp_img
    print img_path
    try:
        img_file = open(img_path)
    except:
        raise Http404
    fw = FileWrapper(img_file)
    os.remove(img_path)
    response = HttpResponse(fw, content_type='image/bmp')
    response['Content-Disposition'] = 'attachment; filename="decrypted_%s"' %  temp_img

    return response


def hill_form(request):
	return render_to_response('hill-form.html', locals(), RequestContext(request))

