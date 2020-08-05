from django.contrib.contenttypes.models import ContentType
from django.contrib.admin.models import LogEntry, ADDITION, CHANGE, DELETION
from django.utils.encoding import force_text

class AuditModel(object):

  def saveLog(self, user, message, ACTION):
    log = LogEntry.objects.create(
      user_id         = user.id,
      content_type_id = ContentType.objects.get_for_model(self).id,
      object_id       = self.id,
      object_repr     = force_text(self),
      action_flag     = ACTION,
      change_message = message
    )

  def saveAddition(self, user, path):
    message = 'url: {}, se ha añadido un nuevo registro'.format(path)
    self.saveLog(user, message, ADDITION)

  def saveEdition(self, user, path):
    message = 'url: {}, se ha modificado el registro'.format(path)
    self.saveLog(user, message, CHANGE)

  def saveDeletion(self, user, path):
    message = 'url: {}, se ha eliminado el registro'.format(path)
    self.saveLog(user, message, DELETION)