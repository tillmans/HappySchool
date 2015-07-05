from django.http import HttpResponse
from django.core.cache import cache
import base64,urllib,urllib2,sys,re,json,random,time
import hashlib

from models import Province,City,District,School,Class,SchoolAdministrator,Teacher,Parents,Kid,Moment,Parent,ParentGroup
from photo.settings import logging

log = logging.getLogger('fun_app')

reload(sys)
sys.setdefaultencoding('gbk')
# Create your views here.

def InvalidUrl(reason):
    response={}
    response['code'] = 400
    response['errorMsg'] = reason
    return HttpResponse(json.dumps(response,ensure_ascii=False),content_type="application/json")

def RightResponse(result)
    response = {}
    response['code'] = 200
    response['result'] = result
    return HttpResponse(json.dumps(response,ensure_ascii=False),content_type="application/json")

def get_cur_func_name():
    """Return the frame object for the caller's stack frame."""
    try:
        raise Exception
    except:
        f = sys.exc_info()[2].tb_frame.f_back
    return f.f_code.co_name

def checkNecessaryParams(request,*paramlist):
    func_name = get_cur_func_name
    if not request:
	log.error('request must not be null when call %s' % func_name)
	raise Exception('request is null when call %s' % func_name)
    method = request.method
    parseResult = {}
    for name in paramlist:
	try:
	    if method == 'GET':
		value = request.GET.get(name).strip(' ')
	    elif method == 'POST':
		value = request.POST.get(name).strip(' ')
	    else:
		log.error('unkown http method when call %s' % func_name)
		errorMsg='unkown http method when call %s' % func_name
		return (1,errorMsg)
	except KeyError,e:
	    log.error('miss necessary parameter %s when call %s' % (name,func_name))
	    errorMsg = 'miss necessary parameter %s when call %s' % (name,func_name)
	    return (1,errorMsg)
	if not value:
	    log.error('%s can not be empty or space when call api %' % (name,request.path))
	    errorMsg = '%s can not be empty when call api %' % (name,request.path)
	    return (1,errorMsg)
	parseResult[name] = value

    log.info('succeeded to check request params %s' % request)
    return (0,parseResult)

def province_list(request):
    provinces = Province.objects.all() 
    result = ' '.join([str(x) for x in provinces])
    return RightResponse(result)

def city_list(request):
    r,out = checkNecessaryParams(request,'province')
    if r:
	return InvalidUrl(out)

    cities = City.objects.filter(province = out['province'])
    if not cities:
	errorMsg='无法在%s找到城市' % (out['province'])
	return InvalidUrl(errorMsg)
    result = ' '.join([str(x) for x in cities])
    return RightResponse(result)

def district_list(request):
    r,out = checkNecessaryParams(request,'province','city')
    if r:
	return InvalidUrl(out)

    city = City.objects.filter(province__name = out['province']).filter(name=out['city'])
    if not city:
	errorMsg='无法在%s找到%s' % (out['province'],out['city'])
	return InvalidUrl(errorMsg)

    districts = city.district_set.all()
    result = ' '.join([str(x) for x in districts])
    return RightResponse(result)

VerifyCodeMap={}

def sendVerifyCode(request):
    r,out = checkNecessaryParams(request,'telephone')
    if r:
	return InvalidUrl(out)

    verify_code = random.randrange(1000,9999,4)
    base64_password = base64.encodestring('774660874')
    content_msg = '【果蔬到家】登陆验证码：'+str(verify_code)+'，请您妥善保管。'
    params = urllib.urlencode({'method':'sendSMS','username':774660874,'password':base64_password,'smstype':'1','mobile':out["telephone"],'isLongSms':'0','content':content_msg})
    url_req = "http://114.215.136.186:9008/servlet/UserServiceAPI"
    sms_req = urllib2.Request(url = url_req, data = params)
    sms_response = urllib2.urlopen(sms_req)
    sms_response=sms_response.read()
    log.debug(sms_response)
    if sms_response[0:3] == 'fail':
	response['code'] = 500
        response['errorMsg'] = '请重新发送验证码~'.decode('gbk').encode('utf8')
        return HttpResponse(json.dumps(response),content_type="application/json")
    #cache.set(str(_telephone),str(verify_code),1800)
    VerifyCodeMap[out['telephone']] = str(verify_code)
    log.info('send_verify_code:'+str(verify_code))
    result='succeeded to send verify code:%s' % str(verify_code)
    return RightResponse(result)


def checkVerifyCode(request):
    r,out=checkNecessaryParams(request,'telephone','code')
    if r:
	return InvalidUrl(out)
    saved_code = VerifyCodeMap[out['telephone']] 
    response={}
    if str(saved_code) == str(out['code']):
	response['code'] = 200
	response['result'] = '验证成功'
	return HttpResponse(json.dumps(response),content_type="application/json")

    response["errorMsg"] = '验证码错误'
    response["code"] = 406
    return HttpResponse(json.dumps(response),content_type="application/json")

def getSchoolAdministratorInfo(request):
    r,out = checkNecessaryParams(request,'telephone')
    if r:
	return InvalidUrl(out)
    sa = SchoolAdministrator.objects.get(telephone = out['telephone'])
    result = {}  
    result[]

def updateSchoolAdministratorPassword(request):
    r,out = checkNecessaryParams(request,'telephone')

def updateTeacherPassword(request):
    pass

def updateParentPassword(request):
    pass

def updateSchoolAdministratorTelephone(request):
    pass

def updateTeacherTelephone(request):
    pass

def updateParentTelephone(request):
    pass

	
def checkTelephone(telephone):
    CM_prog = re.compile(r"^1(34[0-8]|(3[5-9]|5[017-9]|8[278])\d)\d{7}$")
    CU_prog = re.compile(r"^1(3[0-2]|5[256]|8[56])\d{8}$")
    CT_prog = re.compile(r"^1((33|53|8[09])[0-9]|349)\d{7}$")
    telephone_match_CM = CM_prog.match(str(telephone))
    telephone_match_CU = CU_prog.match(str(telephone))
    telephone_match_CT = CT_prog.match(str(telephone))
    if not telephone_match_CM and not telephone_match_CT and not telephone_match_CU:
	return False
    return True

def checkemail(email):
    pattern = re.compile(r'[a-zA-Z]+[a-zA-Z_\.0-9]+@[a-zA-Z0-9]+\.(com|net)')
    if pattern.match(email):
	return True
    return False

def registerSchoolAdministator(request):
    r,out= checkNecessaryParams(request,'name','telephone','email','passwd')
    if r:
	return InvalidUrl(out)
    passwd_hash = hashlib(out['passwd']).hexdigest()
    school_admin = SchoolAdministrator.objects.create(name=out['name'],telephone = out['telephone'],email = name['email'],passwd = passwd_hash)
    school_admin.save()
    result = '成功注册学校管理员,名字:%s 联系电话:%s 邮箱地址:%s' % (owner_name,owner_telephone,owner_email)
    return RightResponse(result)

def createSchool(request):
    try:
	province_name = request.POST.get('province').strip(' ')
	city_name = request.POST.get('city').strip(' ')
	district_name = request.POST.GET('district').strip(' ')
	telephone = request.POST.get('telephone').strip(' ')
	school_name = request.POST.get('schol_name').strip(' ')
    except KeyError,e:
	errorMsg = '缺少某些必选参数'.decode('gbk').encode('utf8')
	return InvalidUrl(errorMsg)
    if province_name and city_name or district_name or owner_name or owner_telephone or owner_email or school_name:
	pass
    else
	errorMsg = '无效的省份或者城市或者区的名字'.decode('gbk').encode('utf8')
	return InvalidUrl(errorMsg)

    district = City.objects.filter(province__name = province_name).filter(name=city_name).filter(districts__name=district_name)
    if not district.exists():
	errorMsg='无法在%s %s找到%s' % (province_name,city_name,district_name)
	return InvalidUrl(errorMsg)
    principal = Principal.objects.create(name=owner_name,telephone = owner_telephone,email = owner_email)
    principal.save()
    school = School.objects.create(name=school_name)
    school.add(principal)
    school.save()
    district.school_set.add(school)
    district.save() 
    result = '成功注册学校:%s 责任人名字:%s 联系电话:%s 邮箱地址:%s' % (school_name,owner_name,owner_telephone,owner_email)
    return RightResponse(result)

def registerTeacher(request):
    try:
	province_name = request.POST.get('province').strip(' ')
	city_name = request.POST.get('city').strip(' ')
	district_name = request.POST.GET('district').strip(' ')
	owner_name = request.POST.get('principal_name').strip(' ')
	owner_telephone = request.POST.get('telephone').strip(' ')
	owner_email = request.POST.get('email').strip(' ')
	school_name = request.POST.get('schol_name').strip(' ')
    except KeyError,e:
	errorMsg = '缺少某些必选参数'.decode('gbk').encode('utf8')
	return InvalidUrl(errorMsg)
    if province_name and city_name or district_name or owner_name or owner_telephone or owner_email or school_name:
	pass
    else
	errorMsg = '无效的省份或者城市或者区的名字'.decode('gbk').encode('utf8')
	return InvalidUrl(errorMsg)

    district = City.objects.filter(province__name = province_name).filter(name=city_name).filter(districts__name=district_name)
    if not district.exists():
	errorMsg='无法在%s %s找到%s' % (province_name,city_name,district_name)
	return InvalidUrl(errorMsg)
    principal = Principal.objects.create(name=owner_name,telephone = owner_telephone,email = owner_email)
    principal.save()
    school = School.objects.create(name=school_name)
    school.add(principal)
    school.save()
    district.school_set.add(school)
    district.save() 
    result = '成功注册学校:%s 责任人名字:%s 联系电话:%s 邮箱地址:%s' % (school_name,owner_name,owner_telephone,owner_email)
    return RightResponse(result)


