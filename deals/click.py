class ClickDeal:

    def __init__(self, request):
        self.session = request.session
        click = self.session.get('click_deal')
        if not click:
            click = self.session['click_deal'] = {}

        self.click = click
        self.session.set_expiry(86400 * 3)

    def action_click(self, deal_id):
        deal_id = str(deal_id)
        # add comment and click to session
        if deal_id not in self.click:
            self.click[deal_id] = 'like'
        self.save()

    def save(self):
        self.session.modified = True


class ClickComment:

    def __init__(self, request):
        self.session = request.session
        click = self.session.get('click')
        if not click:
            click = self.session['click'] = {}

        self.click = click
        self.session.set_expiry(86400)

    def action_click(self, comment_id):
        comment_id = str(comment_id)
        # add comment and click to session
        if comment_id not in self.click:
            self.click[comment_id] = 1
        # delete click from comment
        elif comment_id in self.click and self.click[comment_id] == 1:
            self.click[comment_id] = -1
        # revote the comment
        elif comment_id in self.click and self.click[comment_id] == -1:
            self.click[comment_id] = 1
        self.save()

    def save(self):
        self.session.modified = True

