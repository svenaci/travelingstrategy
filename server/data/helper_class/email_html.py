from email_config import style, message_body, image_left_table_top_tags, image_left_table_bottom_tags, image_right_table_top_tags, image_bottom_tags, footer
class Email_html():
  def __init__(self):
    self.style= style
    self.message_body = message_body
    self.images_left_side = ""
    self.images_right_side = ""

    self.images_left_section = image_left_table_top_tags+self.images_left_side+image_left_table_bottom_tags
    self.image_right_section = image_right_table_top_tags+self.images_right_side+image_bottom_tags
    self.footer = footer

  def get_email(self):
    return "<html>"+self.style+self.message_body+self.images_left_section+self.image_right_section+self.footer+"</html>"

  def add_left_image(self, url, width, height, city):
    additional_image = """
              <tr>
                <th>
                  <table border="0" cellspacing="0" cellpadding="0" role="presentation" style="border-spacing:0;border-collapse:collapse;">
                    <tbody>
                      <tr>
                        <td class="container" style="width:244px;border-collapse:collapse;"><img class="image" data-imagetype="External" src="{}" style="font-size:13px;display:block;width:{}px;height:{}px;text-decoration:none;border:1px solid #EEEEEF;border-top-right-radius:4px;border-bottom-right-radius:4px;border-bottom-left-radius:4px;line-height:13px;outline:none;border-top-left-radius:4px;">
                          <div class="middle">
                            <img data-imagetype="External" src="https://img.icons8.com/offices/30/000000/place-marker.png">{}
                          </div>
                          </a>
                        </td>
                      </tr>
                    </tbody>
                  </table>
                </th>
              </tr>
              <tr>
                <th height="16" style="line-height:0;">&nbsp;</th>
              </tr>
        """.format( url, width, height, city, sep='')
    self.images_left_side = self.images_left_side + additional_image
    self.images_left_section = image_left_table_top_tags+self.images_left_side+image_left_table_bottom_tags

  def add_right_image(self, url, width, height, city):
    additional_image = """
              <tr>
                <th>
                  <table border="0" cellspacing="0" cellpadding="0" role="presentation" style="border-spacing:0;border-collapse:collapse;">
                    <tbody>
                      <tr>
                        <td class="container" style="width:244px;border-collapse:collapse;"><img class="image" data-imagetype="External" src="{}" style="font-size:13px;display:block;width:{}px;height:{}px;text-decoration:none;border:1px solid #EEEEEF;border-top-right-radius:4px;border-bottom-right-radius:4px;border-bottom-left-radius:4px;line-height:13px;outline:none;border-top-left-radius:4px;">
                          <div class="middle">
                            <img data-imagetype="External" src="https://img.icons8.com/offices/30/000000/place-marker.png">{}
                          </div>
                          </a>
                        </td>
                      </tr>
                    </tbody>
                  </table>
                </th>
              </tr>
              <tr>
                <th height="16" style="line-height:0;">&nbsp;</th>
              </tr>
        """.format(url, width, height, city, sep='')
    self.images_right_side = self.images_right_side + additional_image
    self.image_right_section = image_right_table_top_tags+self.images_right_side+image_bottom_tags