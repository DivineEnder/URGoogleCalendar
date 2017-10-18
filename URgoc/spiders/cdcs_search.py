import scrapy
import re

class CDCSSearch(scrapy.Spider):
	name = 'cdcs_search'
	start_urls = ['https://cdcs.ur.rochester.edu/default.aspx']

	def __init__(self, *args,
					ddlTerm,
					ddlSchool = '',
					ddlDept = '',
					txtCourse = '',
					ddlTypes = '',
					ddlStatus = '',
					txtDescription = '',
					txtTitle = '',
					txtInstructor = '',
					ddlTimeFrom = '',
					ddlTimeTo = '',
					ddlCreditFrom = '',
					ddlCreditTo = '',
					ddlDivision = '', **kwargs):
		self.ddlTerm = ddlTerm
		self.ddlSchool = ddlSchool
		self.ddlDept = ddlDept
		self.txtCourse = txtCourse
		self.ddlTypes = ddlTypes
		self.ddlStatus = ddlStatus
		self.txtDescription = txtDescription
		self.txtTitle = txtTitle
		self.txtInstructor = txtInstructor
		self.ddlTimeFrom = ddlTimeFrom
		self.ddlTimeTo = ddlTimeTo
		self.ddlCreditFrom = ddlCreditFrom
		self.ddlCreditTo = ddlCreditTo
		self.ddlDivision = ddlDivision

	def parse(self, response):
		yield scrapy.FormRequest(
			'https://cdcs.ur.rochester.edu/default.aspx',
			formdata={
				'ddlTerm': self.ddlTerm,
				'ddlSchool': self.ddlSchool,
				'ddlDept': self.ddlDept,
				'txtCourse': self.txtCourse,
				'ddlTypes': self.ddlTypes,
				'ddlStatus': self.ddlStatus,
				'txtDescription': self.txtDescription,
				'txtTitle': self.txtTitle,
				'txtInstructor': self.txtInstructor,
				'ddlTimeFrom': self.ddlTimeFrom,
				'ddlTimeTo': self.ddlTimeTo,
				'ddlCreditFrom': self.ddlCreditFrom,
				'ddlCreditTo': self.ddlCreditTo,
				'ddlDivision': self.ddlDivision,
				'ScriptManager1': 'UpdatePanel4|btnSearchTop',
				'btnSearchTop': "Search",
				'__ASYNCPOST': 'false',
				'__LASTFOCUS': '',
				'__EVENTTARGET': '',
				'__EVENTARGUMENT': '',
				'__VIEWSTATE': response.css('input#__VIEWSTATE::attr(value)').extract_first(),
				'__VIEWSTATEGENERATOR': response.css('input#__VIEWSTATEGENERATOR::attr(value)').extract_first(),
				'__EVENTVALIDATION': response.css('input#__EVENTVALIDATION::attr(value)').extract_first()
			},
			callback = self.parse_results
		)

	def parse_results(self, response):
		with open("results.html", "wb") as file:
			file.write(response.body)

		for course in response.xpath('//td[@class="repeaterHead"]/../..'):
			course_info = {}
			for item in course.css('span'):
				key = re.match(r'(.*)_lbl(.*)', item.css('::attr(id)').extract_first()).group(2)
				value = item.css('::text').extract_first()
				course_info[key] = value
				# print("Course['%s'] = '%s'" % (key, value))
			yield course_info
			# for item in course.css('td'):
			# 	print(item)
			# 	if item.css('span').extract_first() is not None:
			# 		id = item.css('span::attr(id)').extract_first()
			# 		print("SPAN ID: " + id)
			# 		key = re.match(r'(.*)_lbl(.*)', id)
			# 		print(key)
			# 		print("Should put %s into map with key '%s'" % (item.css('span::text').extract_first(), key.group(2)))
			# 	else:
			# 		print("The sub dictionary should be stored under '%s'" % (item.css('::text').extract_first()))
			# 	input()
