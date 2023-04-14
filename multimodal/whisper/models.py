from django.utils.timezone import now

from django.db import models

# Create your models here.


# class Lang(models.Model):
#     id = models.AutoField(primary_key=True)
#     lang_short = models.CharField(max_length=3)
#     lang_long = models.CharField(max_length=50)

class Whisper(models.Model):
    MODEL_OPTIONS = [('tiny.en','tiny.en'),('tiny','tiny'),('base.en','base.en'),('base','base'),('small.en','small.en'),(' ','small'),('medium.en','medium.en'),('medium','medium'),('large-v1','large-v1'),('large-v2','large-v2'),('large','large')]
    TASK_OPTIONS = [('transcribe','transcribe'), ('Translate','translate')]
    OUTPUT_FORMAT = [('all','all'),('Text','txt'),('Vtt','vtt'),('Srt','srt'),('Tsv','tsv'),('Json','json')]
    LANG_OPTIONS = [('Afrikaans','Afrikaans'),('Amharic','Amharic'),('Arabic','Arabic'),('Assamese','Assamese'),('Azerbaijani','Azerbaijani'),('Bashkir','Bashkir'),('Belarusian','Belarusian'),('Bengali','Bengali'),('Bosnian','Bosnian'),('Breton','Breton'),('Bulgarian','Bulgarian'),('Burmese','Burmese'),('Castilian','Castilian'),('Catalan','Catalan'),('Chinese','Chinese'),('Croatian','Croatian'),('Czech','Czech'),('Danish','Danish'),('Dutch','Dutch'),('English','English'),('Estonian','Estonian'),('Faroese','Faroese'),('Finnish','Finnish'),('Flemish','Flemish'),('French','French'),('Galician','Galician'),('Georgian','Georgian'),('German','German'),('Greek','Greek'),('Gujarati','Gujarati'),('Haitian','Haitian'),('Haitian Creole','Haitian Creole'),('Hausa','Hausa'),('Hawaiian','Hawaiian'),('Hebrew','Hebrew'),('Hindi','Hindi'),('Hungarian','Hungarian'),('Icelandic','Icelandic'),('Indonesian','Indonesian'),('Italian','Italian'),('Japanese','Japanese'),('Javanese','Javanese'),('Kannada','Kannada'),('Kazakh','Kazakh'),('Khmer','Khmer'),('Korean','Korean'),('Lao','Lao'),('Latin','Latin'),('Latvian','Latvian'),('Letzeburgesch','Letzeburgesch'),('Lingala','Lingala'),('Lithuanian','Lithuanian'),('Luxembourgish','Luxembourgish'),('Macedonian','Macedonian'),('Malagasy','Malagasy'),('Malay','Malay'),('Malayalam','Malayalam'),('Maltese','Maltese'),('Maori','Maori'),('Marathi','Marathi'),('Moldavian','Moldavian'),('Moldovan','Moldovan'),('Mongolian','Mongolian'),('Myanmar','Myanmar'),('Nepali','Nepali'),('Norwegian','Norwegian'),('Nynorsk','Nynorsk'),('Occitan','Occitan'),('Panjabi','Panjabi'),('Pashto','Pashto'),('Persian','Persian'),('Polish','Polish'),('Portuguese','Portuguese'),('Punjabi','Punjabi'),('Pushto','Pushto'),('Romanian','Romanian'),('Russian','Russian'),('Sanskrit','Sanskrit'),('Serbian','Serbian'),('Shona','Shona'),('Sindhi','Sindhi'),('Sinhala','Sinhala'),('Sinhalese','Sinhalese'),('Slovak','Slovak'),('Slovenian','Slovenian'),('Somali','Somali'),('Spanish','Spanish'),('Sundanese','Sundanese'),('Swahili','Swahili'),('Swedish','Swedish'),('Tagalog','Tagalog'),('Tajik','Tajik'),('Tamil','Tamil'),('Tatar','Tatar'),('Telugu','Telugu'),('Thai','Thai'),('Tibetan','Tibetan'),('Turkish','Turkish'),('Turkmen','Turkmen'),('Ukrainian','Ukrainian'),('Urdu','Urdu'),('Uzbek','Uzbek'),('Valencian','Valencian'),('Vietnamese','Vietnamese'),('Welsh','Welsh'),('Yiddish','Yiddish'),('Yoruba','Yoruba')]
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)
    model = models.CharField(max_length=10, choices=MODEL_OPTIONS, blank=False, )
    output_format= models.CharField(max_length=5, choices=OUTPUT_FORMAT, blank=False)
    task = models.CharField(max_length=10, choices=TASK_OPTIONS, blank=False)
    language = models.CharField(max_length=50, choices=LANG_OPTIONS, blank=False)
    upload_file = models.FileField(upload_to='documents/', default='images/MPI_logo_regular.png')
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name
