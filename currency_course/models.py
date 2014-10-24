"""Models for the currency_course app."""
from django.db import models
from django.utils.translation import ugettext_lazy as _


class Currency(models.Model):
    """
    Contains information about one currency.

    :iso_code: ISO-4217-Code of the currency (e.g. EUR).
    :title: Official title of the currency.
    :abbreviation: Abbreviation of the currency title.

    """
    iso_code = models.CharField(
        verbose_name=_('ISO-code'),
        max_length=3,
        unique=True,
    )

    title = models.CharField(
        verbose_name=_('Title'),
        max_length=50,
    )

    abbreviation = models.CharField(
        verbose_name=_('Abbreviation'),
        max_length=10,
        help_text=_(u'e.g. \u20AC or \u0024'),
        blank=True,
    )

    class Meta:
        ordering = ['iso_code']

    def save(self, *args, **kwargs):
        self.iso_code = self.iso_code.upper()
        super(Currency, self).save(*args, **kwargs)

    def __unicode__(self):
        return self.iso_code


class CurrencyCourse(models.Model):
    """
    Connects two currencies to a course.

    :from_currency: Currency to convert.
    :to_currency: Currency to be converted to.

    """
    from_currency = models.ForeignKey(
        Currency,
        verbose_name=_('From currency'),
        related_name='courses_from',
    )

    to_currency = models.ForeignKey(
        Currency,
        verbose_name=_('To currency'),
        related_name='courses_to',
    )

    class Meta:
        ordering = ['from_currency__iso_code', 'to_currency__iso_code']

    def __unicode__(self):
        return u'{} - {}'.format(self.from_currency, self.to_currency)

    def latest(self):
        try:
            return self.history.all()[0]
        except IndexError:
            return None


class CurrencyCourseHistory(models.Model):
    """
    Tracks a course status.

    :course: The tracked course.
    :date: Date the status was tracked.
    :value: Value of the second currency in relation to the first.
    :tracked_by: Field to track a service or user who added the history.

    """
    course = models.ForeignKey(
        CurrencyCourse,
        verbose_name=_('Course'),
        related_name='history',
    )

    date = models.DateTimeField(
        verbose_name=_('Date'),
        auto_now_add=True,
    )

    value = models.FloatField(
        verbose_name=_('Value'),
        help_text=_('Value of the second currency in relation to the first.'),
    )

    tracked_by = models.CharField(
        max_length=512,
        verbose_name=_('Tracked by'),
        default=_('Add your email'),
    )

    class Meta:
        ordering = ['-date', 'course__to_currency__iso_code']

    def __unicode__(self):
        return u'{} / {}'.format(self.course, self.date)
