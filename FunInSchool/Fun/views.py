from django.http import HttpResponse
from django.core.cache import cache
import base64,urllib,urllib2,sys,re,json,random,time
import hashlib

from models import Province,City,District,School,Class,SchoolAdministrator,Teacher,Parents,Kid,Moment,Parent,ParentGroup
from FunInSchool.settings import logging
from django.core.mail import send_mail

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
    result['name'] = sa.name
    result['telephone'] = sa.telephone
    result['email'] = sa.email
    result = json.dumps(result)
    return RightResponse(result)

def updateSchoolAdministratorPassword(request):
    r,out = checkNecessaryParams(request,'telephone','passwd')
    if r:
	return InvalidUrl(out)
    sa = SchoolAdministrator.objects.get(telephone = out['telephone'])
    hash_passwd = hashlib(out['passwd']).hexdigest()
    sa.passwd = hash_passwd
    sa.save()
    result="succeeded to update %s's password" % (sa.name)
    return RightResponse(result)

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

#-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------

def registerSchoolAdministator(request):
    #学校管理权限较大，注册为学校管理员时需要有控制机制
    r,out= checkNecessaryParams(request,'name','telephone','email','passwd','id_card')
    if r:
	return InvalidUrl(out)
    passwd_hash = hashlib(out['passwd']).hexdigest()
    school_admin = SchoolAdministrator.objects.create(name=out['name'],telephone = out['telephone'],email = name['email'],passwd = passwd_hash,id_card=out['id_card'])
    school_admin.save()
    result = '成功注册学校管理员,名字:%s 联系电话:%s 邮箱地址:%s' % (owner_name,owner_telephone,owner_email)
    return RightResponse(result)

def querySchoolAdministrator(request):
    pass

def updateSchoolAdministrator(request):
    pass

def deleteSchoolAdministrator(request):
    pass

#-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------

def createSchool(request):
    r,out = checkNecessaryParams(request,'province','city','district','telephone','school_name','address')
    if r:
	return InvalidUrl(errorMsg)

    try:
	district = City.objects.filter(province__name = out['province']).filter(name=out['city']).filter(districts__name=out['district'])
    except DoesNotExist,e:
	errorMsg='无法在%s %s找到%s,%s' % (out['province'],out['city'],out['district'],e)
	return InvalidUrl(errorMsg)
    #检查是否是学校管理员电话 
    try:
	sa = SchoolAdministrator.objects.get(telephone = out[telephone])
    except DoesNotExist,e:
	errorMsg='the current user is not a school administrator,only school administrators can create school'
	return InvalidUrl(errorMsg)
    school = School(address = out['address'],name = out['school_name'],status='EI')
    school.save()
    try:
	district.add(school)
	sa.add(school)
    except:
	errorMsg = 'can not add the current school to %s or %s' % (district.name,sa.name)
	return InvalidUrl(errorMsg)
	
    result = '成功注册学校:%s 责任人名字:%s 地区:%s,状态审核中,我们将尽快完成对该学校合法性的审核' % (out['school_name'],sa.name,district.name)
    #后台人员审核通过之后将学校状态置为审核通过
    return RightResponse(result)

def updateSchool(request):
    pass

def querySchool(request):
    pass

def deleteSchool(request):
    pass

#-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------

def createClass(request):
    r,out = checkNecessaryParams(request,'province','city','district','telephone','school_name','name')
    if r:
	return InvalidUrl(errorMsg)

    try:
	district = City.objects.filter(province__name = out['province']).filter(name=out['city']).filter(districts__name=out['district'])
    except DoesNotExist,e:
	errorMsg='无法在%s %s找到%s,%s' % (out['province'],out['city'],out['district'],e)
	return InvalidUrl(errorMsg)

    #检查是否是学校管理员电话 
    try:
	sa = SchoolAdministrator.objects.get(telephone = out[telephone])
    except DoesNotExist,e:
	errorMsg='the current user is not a school administrator,only school administrators can create school'
	return InvalidUrl(errorMsg)

    try:
	school = district.school_set.get(school__name = out['school_name'])
    except DoesNotExist,e:
	errorMsg='can not find school %s in district %s' % (out['school_name'],out['district'])
	return InvalidUrl(errorMsg)
    school_class = Class(name = out['name'])
    school_class.save() 
    school.add(school_class)
    school.save()	
    result = '成功创建班级:%s 学校:%s 学校负责人:%s' % (out['name'],out['school_name'],sa.name)
    return RightResponse(result)

def updateClass(request):
    pass

def queryClass(request):
    pass

def deleteClass(request):
    pass


#-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------

def registerTeacher(request):
    #假设同一个区域的学校名字不重复
    r,out = checkNecessaryParams(request,'provice','city','district','school_name','telephone','email','class_name','name')
    if r:
	return InvalidUrl(out)
    try:
	district = City.objects.filter(province__name = province_name).filter(name=city_name).filter(districts__name=district_name)
    except DoesNotExist,e:
	errorMsg='无法在%s %s找到%s,%s' % (province_name,city_name,district_name,e)
	return InvalidUrl(errorMsg)
    try:
	school = district.filter(school__name=out['school_name'])
    except DoesNotExist,e:
	errorMsg = "can not find school %s in %s" % (out['school_name'],out['district'])
	return InvalidUrl(errorMsg)

    try:
	class_id = school.filter(class__name=out['class_name'])
    except DoesNotExist,e:
	errorMsg = "can not find class %s in school %s" % (out['class_name'],out['school_name'])
	return InvalidUrl(errorMsg)

    tea = Teacher(name=out['name'],telephone=out['telephone'],email = out['email'],status='NE') 
    tea.save() 
    class_id.add(tea)
    class_id.save()
    tea.status='EI'
    #发送url给学校管理员的邮箱对新注册的老师进行审核
    url_yes=''
    url_no=''
    mail_title = '幼儿园教师注册审核'
    mail_content = '教师%s 头像预留正在注册为你的学校%s的教师，请点击下面链接确认是否同意:\n\t同意链接:%s，拒绝链接:%s' % (out['name'],out['school_name'],url_yes,url_no)
    from_mail = 'tju.zk@163.com'
    to_mail = ['tju.zk@163.com']
    #这里需要考虑发送邮件失败的情况，目前暂时未处理
    send_mail(mail_title,mail_content,from_mail,to_mail,fail_silently = False)
    
    tea.status='EI'
    tea.save() 
    result = '成功注册老师到班级:%s 老师名字:%s 联系电话:%s 邮箱地址:%s,目前由学校管理员审核中' % (out['class_name'],out['name'],out['telephone'],out['email'])
    return RightResponse(result)

def OnPassTeacherRegister(request):
    #修改教师状态为审核通过
    pass

def OnRejectTeacherRegister(request):
   #从数据库中删除该教师信息 
   pass

def UpdateTeacher(requst):
    #更新教师个人信息
    #将request中教师的信息与数据库中的信息逐个做比较，更新有差异的条目
    pass

def queryTeacher(request):
    pass

def deleteTeacher(request):
    pass


#-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------

def createKid(request):
    #假设同一个区域的学校名字不重复
    #教师创建kid
    pass

def updateKid(request):
    pass

def queryKid(request):
    #读取kid的信息
    pass

def deleteKid(request):
    #删除kid
    pass


#-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------

def registerParents(request):
    #注册家长
    pass

def updateParents(request):
    #更新家长的信息
    pass

def queryParents(request):
    #获取家长的信息
    pass

def deleteParents(request):
    #删除家长的信息
    pass
