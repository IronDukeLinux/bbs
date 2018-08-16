# '2018/8/15 15:39'
# coding=utf-8


class MyPage(object):
    def __init__(self, current_page, total_count, base_url, per_page=10, max_show=11):
        """
        :param current_page: 当前页
        :param total_count: 数据库中数据总数
        :param per_page: 每页显示多少条数据
        :param max_show: 最多显示多少页
        """
        try:
            current_page = int(current_page)
        except ValueError as e:
            current_page = 1

        self.current_page = current_page
        self.total_count = total_count
        self.base_url = base_url
        self.per_page = per_page
        self.max_show = max_show

        # 总页码
        total_page, more = divmod(total_count, per_page)
        if more:
            total_page += 1

        half_show = int((max_show - 1) / 2)
        self.half_show = half_show
        self.total_page = total_page

    @property
    def start(self):
        return (self.current_page - 1) * self.per_page

    @property
    def end(self):
        return self.current_page * self.per_page

    def page_html(self):

        if self.current_page <= self.half_show:
            show_start = 1
            show_end = self.max_show
        else:
            if self.current_page + self.half_show >= self.total_page:
                show_start = self.total_page - self.max_show
                show_end = self.total_page
            else:
                show_start = self.current_page - self.half_show
                show_end = self.current_page + self.half_show

                # 生成页面上显示的页码
        page_html_list = []
        # 加首页
        first_li = '<li><a href="{}?page=1">首页</a></li>'.format(self.base_url)
        page_html_list.append(first_li)
        # 加上一页
        if self.current_page == 1:
            prev_li = '<li><a href="#">上一页</a></li>'
        else:
            prev_li = '<li><a href="{0}?page={1}">上一页</a></li>'.format(self.base_url, self.current_page - 1)
        page_html_list.append(prev_li)
        for i in range(show_start, show_end + 1):
            if i == self.current_page:
                li_tag = '<li class="active"><a href="{0}?page={1}">{1}</a></li>'.format(self.base_url, i)
            else:
                li_tag = '<li><a href="{0}?page={1}">{1}</a></li>'.format(self.base_url, i)
            page_html_list.append(li_tag)

        # 加下一页
        if self.current_page == self.total_page:
            next_li = '<li><a href="#">下一页</a></li>'
        else:
            next_li = '<li><a href="{0}?page={1}">下一页</a></li>'.format(self.base_url, self.current_page + 1)
        page_html_list.append(next_li)

        # 加尾页
        page_end_li = '<li><a href="{0}?page={1}">尾页</a></li>'.format(self.base_url, self.total_page)
        page_html_list.append(page_end_li)

        return '<nav aria-label="Page navigation"><ul class="pagination">'+"".join(page_html_list)+'</ul></nav>'
