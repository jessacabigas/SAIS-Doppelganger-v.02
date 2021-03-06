from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.views.generic import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponse, HttpResponseRedirect
from django.views.generic import View, DetailView
from WebApp.models import Student, SchoolInfo, Subjects
from django.template import Context

class IndexView(View):
	
	def get(self, request):	
		return render(self.request, 'main.html')

class StudentViewSchedule(View):

	def get(self, request):
		context = {}
		context['user'] = request.user.first_name
		return render(self.request,'indexStudent-Schedule.html',context=context)

class StudentViewAccount(View):

	def get(self, request):
		context = {}
		context['user'] = request.user.first_name
		return render(self.request,'indexStudent-Account.html',context=context)

class StudentEnlist(View):

	def get(self, request):
		context = {}
		context['user'] = request.user.first_name
		return render(self.request, 'indexStudent-Enlist.html', context=context)


	def post(self, request):

		keyword = request.POST.get('searchbox')
		print("Keyword is: " + keyword)
		context = {}
		context['subjectcode'] = Subjects.objects.filter(subject_code__icontains=keyword)
		return render(self.request,'indexStudent-Enlist.html',context=context)

class StudentView(View):
	def get(self, request):
		if not request.user.is_authenticated():
			return render(self.request, 'login.html')
		else:
			 student_object = Student.objects.filter(user_id=request.user)
			 schoolinfo_object = SchoolInfo.objects.filter(student_id=student_object)
			
		   
			 dictionary = {
		    	'firstname': student_object.get().fname,
		    	'middlename': student_object.get().mname,
		    	'lastname': student_object.get().lname,
		    	'address': student_object.get().address,
		    	'gender': student_object.get().gender,
		    	'maritalstatus': student_object.get().maritalstatus,
		    	'student_id': student_object.get().student_id,
		    	'email': student_object.get().email,
		    	'course': schoolinfo_object.get().course,
		    	'year': schoolinfo_object.get().year,
		    	'sts_code': schoolinfo_object.get().sts_code,
		    	'user': request.user.first_name,
		    	}
		
		return render(self.request,'indexStudent-Profile.html',dictionary)

class LoginView(View):
	"""docstring for LoginView"""
	def get(self, request):
		if not request.user.is_authenticated():
			return render(self.request, 'login.html')
		else:
			return render(self.request, 'indexStudent-Profile.html')

	def post(self, request):
		user = User()
		username = request.POST.get('student_id')
		password = request.POST.get('password')
		user = authenticate(username = username, password =password)
		if user is not None:
		    # the password verified for the user		
		  		login(request, user)
		  		return HttpResponseRedirect('../WebApp/profile') 
		 
		else:  # Return an 'invalid login' error message.
			print("The username and password were incorrect.")
			return render(self.request, 'login.html')

class LogoutView(View):
	def get(self, request):
		return redirect('WebApp:logout')	

	def post(self, request):
		logout(request, user)

class RegistrationView(View):
	
	def get(self, request):
		return render(self.request, 'register.html')

	def post(self, request):
		student = Student()
		studentInfo = SchoolInfo()
		
		student.fname = request.POST['fname']
		student.mname = request.POST['mname']
		student.lname = request.POST['lname']
		student.student_id = request.POST['student_id']
		student.address = request.POST['address']
		student.gender = request.POST['gender']
		student.maritalstatus = request.POST['maritalstatus']
		student.email = request.POST['email']
		student.save()

		studentInfo.student_id = student
		studentInfo.course = request.POST['course']
		studentInfo.year = request.POST['year']
		studentInfo.sts_code = request.POST['sts_code']
		studentInfo.save()

		user = User.objects.create_user(student.student_id, student.email, request.POST['password'])
		
		user.last_name = student.lname
		user.first_name = student.fname
		user.save()
		print(user.username)

		student.user_id = user;
		student.save()

		return render(self.request, 'login.html')

class SearchClassView(View):

	def get(self, request):
		return render(self.request, 'AddClass.html')

	def post(self, request):
		keyword = request.POST.get('searchbox')
		print("Keyword is: " + keyword)
		context = {}
		context['subjectcode'] = Subjects.objects.filter(subject_code__icontains=keyword)
		return render(self.request,'AddClass.html',context=context)


class EditView(View):
	
	def get(self, request):
		if request.user.is_authenticated():
		    student_object = Student.objects.filter(user_id=request.user)
		    schoolinfo_object = SchoolInfo.objects.filter(student_id=student_object)
		    dictionary = {
		    	'firstname': student_object.get().fname,
		    	'middlename': student_object.get().mname,
		    	'lastname': student_object.get().lname,
		    	'address': student_object.get().address,
		    	'gender': student_object.get().gender,
		    	'maritalstatus': student_object.get().maritalstatus,
		    	'student_id': student_object.get().student_id,
		    	'email': student_object.get().email,
		    	'course': schoolinfo_object.get().course,
		    	'year': schoolinfo_object.get().year,
		    	'sts_code': schoolinfo_object.get().sts_code,
		    	'user': request.user.first_name,

		    	}
		    return render(self.request, 'EditProfile.html', dictionary)
		else:
			return render(self.request, 'login.html')

	def post(self, request):

		#Entry.objects.filter(pub_date__year=2007).update(headline='Everything is the same')
		student_objects = Student.objects.filter(user_id=request.user)
		schoolinfo_objects = SchoolInfo.objects.filter(student_id=student_objects)
		print("I AM HERE!!" + student_objects.get().lname)
		firstname = request.POST['fname']
		middlename = request.POST['mname']
		lastname = request.POST['lname']
		address = request.POST['address']
		gender = request.POST['gender']
		maritalstatus = request.POST['maritalstatus']
		email = request.POST['email']
		course = request.POST['course']
		year = request.POST['year']

		student_objects.update(fname = firstname)
		student_objects.update(mname = middlename)
		student_objects.update(lname = lastname)
		student_objects.update(address = address)
		student_objects.update(gender = gender)
		student_objects.update(maritalstatus = maritalstatus)
		
		student_objects.update(email = email)
		schoolinfo_objects.update(course=course)
		schoolinfo_objects.update(year=year)

		return HttpResponseRedirect('../WebApp/profile') 

	
		
