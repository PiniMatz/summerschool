# -*- coding: utf-8 -*-
"""
לוח שיעורים אינטראקטיבי - בית הספר של החופש הגדול יולי 2026
--------------------------------------------------------------
הוראות שימוש בגוגל קולאב (Google Colab):
1. פתחו מחברת חדשה בגוגל קולאב (https://colab.research.google.com)
2. העתיקו את כל הקוד שבקובץ זה והדביקו אותו בתא קוד (Code cell) ריק.
3. לחצו על כפתור ה-Play (הרצה) בצד שמאל של התא.
4. הזינו שם תלמיד/ה או שם קבוצה בתיבת הטקסט שתיפתח, ותקבלו את לוח השעות האישי שלהם.
"""

import json
import re
import difflib

# ==============================================================
# הגדרות תצוגה לעברית (HEBREW DISPLAY SETTINGS)
# ==============================================================
# אם העברית במחברת מוצגת הפוך (משמאל לימין, למשל "רנצמ רהס" במקום "סהר מצנר"),
# שנו הגדרה זו ל-True כדי להפוך את כיוון הטקסט אוטומטית:
REVERSE_HEBREW = False
# ==============================================================

# 1. מאגר השיעורים המלא (הורד מהקבצים)
SESSIONS_JSON = '''[
  {
    "week": 1,
    "day_header": "יום רביעי 1.7",
    "day_name": "יום רביעי",
    "date": "1.7",
    "file": "_תכנון שבועי 1 בית ספר של החופש הגדול כיתות ד-ו.docx",
    "sessions": [
      {
        "group": "ד (קב' 2)",
        "time": "10.00-11.30",
        "subject": "שפה עם שחר",
        "row": "ד"
      },
      {
        "group": "ד (קב' 2)",
        "time": "11.30-13.00",
        "subject": "העשרה באומנות עם מירב צ.",
        "row": "ד"
      },
      {
        "group": "ד (קב' 3)",
        "time": "8.00-9.30",
        "subject": "שפה עם שחר",
        "row": "ד"
      },
      {
        "group": "ד (קב' 3)",
        "time": "10.00-11.30",
        "subject": "העשרה באומנות עם מירב צ.",
        "row": "ד"
      },
      {
        "group": "ה+ו",
        "time": "8.00-9.00",
        "subject": "העשרה באומנות עם מירב צ.",
        "row": "ה+ו"
      },
      {
        "group": "ה (ה' 9)",
        "time": "9.00-11.00",
        "subject": "שפה עם שרון",
        "row": "ה+ו"
      },
      {
        "group": "ו",
        "time": "9.00-11.00",
        "subject": "שפה עם רינת",
        "row": "ה+ו"
      }
    ]
  },
  {
    "week": 1,
    "day_header": "יום חמישי 2.7",
    "day_name": "יום חמישי",
    "date": "2.7",
    "file": "_תכנון שבועי 1 בית ספר של החופש הגדול כיתות ד-ו.docx",
    "sessions": [
      {
        "group": "ד (קב' 1)",
        "time": "8.00-9.30",
        "subject": "מתמטיקה עם מירב א.",
        "row": "ד"
      },
      {
        "group": "ד (קב' 1)",
        "time": "10.00-11.30",
        "subject": "שפה עם שחר",
        "row": "ד"
      },
      {
        "group": "ד (קב' 2)",
        "time": "8.00-9.30",
        "subject": "שפה עם שחר",
        "row": "ד"
      },
      {
        "group": "ד (קב' 2)",
        "time": "10.00-12.00",
        "subject": "מתמטיקה עם מירב א.",
        "row": "ד"
      },
      {
        "group": "ד (קב' 3)",
        "time": "11.30-13.00",
        "subject": "שפה עם שחר",
        "row": "ד"
      },
      {
        "group": "ה (ה' 8)",
        "time": "8.00-9.30",
        "subject": "שפה עם רינת",
        "row": "ה+ו"
      },
      {
        "group": "ו",
        "time": "9.30-11.00",
        "subject": "שפה עם רינת",
        "row": "ה+ו"
      }
    ]
  },
  {
    "week": 2,
    "day_header": "יום ראשון 5.7",
    "day_name": "יום ראשון",
    "date": "5.7",
    "file": "_תכנון שבועי 2 בית ספר של החופש הגדול כיתות ד-ו.docx",
    "sessions": [
      {
        "group": "ד (קב' 3)",
        "time": "10.00-12.00",
        "subject": "מתמטיקה עם מירב א.",
        "row": "ד"
      },
      {
        "group": "ה (ה' 8)",
        "time": "8.00-9.30",
        "subject": "מתמטיקה עם מירב א.",
        "row": "ה+ו"
      },
      {
        "group": "ה (ה' 8)",
        "time": "10.00-11.30",
        "subject": "שפה עם רינת",
        "row": "ה+ו"
      },
      {
        "group": "ו",
        "time": "10.00-11.30",
        "subject": "שפה עם רינת",
        "row": "ה+ו"
      }
    ]
  },
  {
    "week": 2,
    "day_header": "יום שני 6.7",
    "day_name": "יום שני",
    "date": "6.7",
    "file": "_תכנון שבועי 2 בית ספר של החופש הגדול כיתות ד-ו.docx",
    "sessions": [
      {
        "group": "ד (קב' 1)",
        "time": "8.00-9.30",
        "subject": "מתמטיקה עם מירב א.",
        "row": "ד"
      },
      {
        "group": "ד (קב' 1)",
        "time": "10.00-11.30",
        "subject": "שפה עם שרון",
        "row": "ד"
      },
      {
        "group": "ד (קב' 2)",
        "time": "8.00-9.30",
        "subject": "שפה עם שרון",
        "row": "ד"
      },
      {
        "group": "ד (קב' 2)",
        "time": "10.00-11.30",
        "subject": "מתמטיקה עם מירב א.",
        "row": "ד"
      },
      {
        "group": "ו",
        "time": "8.00-9.30",
        "subject": "שפה עם רינת",
        "row": "ה+ו"
      },
      {
        "group": "ה",
        "time": "10.00-11.30",
        "subject": "שפה עם רינת",
        "row": "ה+ו"
      }
    ]
  },
  {
    "week": 2,
    "day_header": "יום שלישי 7.7",
    "day_name": "יום שלישי",
    "date": "7.7",
    "file": "_תכנון שבועי 2 בית ספר של החופש הגדול כיתות ד-ו.docx",
    "sessions": [
      {
        "group": "ד (קב' 1)",
        "time": "8.00-9.30",
        "subject": "שפה עם מיכל ש.",
        "row": "ד"
      },
      {
        "group": "ד (קב' 2)",
        "time": "10.00-11.30",
        "subject": "שפה עם מיכל ש.",
        "row": "ד"
      },
      {
        "group": "ד (קב' 3)",
        "time": "12.00-13.00",
        "subject": "שפה עם מיכל ש.",
        "row": "ד"
      },
      {
        "group": "ה",
        "time": "8.00-9.30",
        "subject": "מתמטיקה עם מירב א.",
        "row": "ה+ו"
      },
      {
        "group": "ה",
        "time": "10.00-11.30",
        "subject": "שפה עם שרון",
        "row": "ה+ו"
      },
      {
        "group": "ו",
        "time": "8.00-9.30",
        "subject": "שפה עם שרון",
        "row": "ה+ו"
      },
      {
        "group": "ו",
        "time": "10.00-11.30",
        "subject": "מתמטיקה עם מירב א.",
        "row": "ה+ו"
      }
    ]
  },
  {
    "week": 2,
    "day_header": "יום רביעי 8.7",
    "day_name": "יום רביעי",
    "date": "8.7",
    "file": "_תכנון שבועי 2 בית ספר של החופש הגדול כיתות ד-ו.docx",
    "sessions": [
      {
        "group": "ד (קב' 3)",
        "time": "8.00-9.30",
        "subject": "שפה עם מיכל ש.",
        "row": "ד"
      },
      {
        "group": "ד (קב' 1)",
        "time": "10.00-11.30",
        "subject": "שפה עם מיכל ש.",
        "row": "ד"
      },
      {
        "group": "ד (קב' 2)",
        "time": "12.00-13.00",
        "subject": "שפה עם מיכל ש.",
        "row": "ד"
      },
      {
        "group": "ה",
        "time": "8.00-9.30",
        "subject": "שפה עם שרון",
        "row": "ה+ו"
      },
      {
        "group": "ו",
        "time": "10.00-11.30",
        "subject": "שפה עם שרון",
        "row": "ה+ו"
      }
    ]
  },
  {
    "week": 2,
    "day_header": "יום חמישי 9.7",
    "day_name": "יום חמישי",
    "date": "9.7",
    "file": "_תכנון שבועי 2 בית ספר של החופש הגדול כיתות ד-ו.docx",
    "sessions": [
      {
        "group": "ד (קב' 1)",
        "time": "8.00-9.30",
        "subject": "מתמטיקה עם מירב א.",
        "row": "ד"
      },
      {
        "group": "ד (קב' 2)",
        "time": "10.00-12.00",
        "subject": "מתמטיקה עם מירב א.",
        "row": "ד"
      }
    ]
  },
  {
    "week": 3,
    "day_header": "יום ראשון 12.7",
    "day_name": "יום ראשון",
    "date": "12.7",
    "file": "_תכנון שבועי 3 בית ספר של החופש הגדול כיתות ד-ו.docx",
    "sessions": [
      {
        "group": "ד (קב' 2)",
        "time": "8.00-9.30",
        "subject": "שפה עם מיכל ש.",
        "row": "ד"
      },
      {
        "group": "ד (קב' 3)",
        "time": "10.00-11.30",
        "subject": "שפה עם מיכל ש.",
        "row": "ד"
      },
      {
        "group": "ד (קב' 1)",
        "time": "12.00-13.00",
        "subject": "שפה עם מיכל ש.",
        "row": "ד"
      }
    ]
  },
  {
    "week": 3,
    "day_header": "יום שני 13.7",
    "day_name": "יום שני",
    "date": "13.7",
    "file": "_תכנון שבועי 3 בית ספר של החופש הגדול כיתות ד-ו.docx",
    "sessions": [
      {
        "group": "ד (קב' 1)",
        "time": "8.00-9.30",
        "subject": "שפה עם שחר",
        "row": "ד"
      },
      {
        "group": "ד (קב' 2)",
        "time": "10.00-11.30",
        "subject": "שפה עם שחר",
        "row": "ד"
      },
      {
        "group": "ד (קב' 2)",
        "time": "12.00-13.00",
        "subject": "שפה עם שחר",
        "row": "ד"
      },
      {
        "group": "ו",
        "time": "8.00-9.30",
        "subject": "שפה עם שרון",
        "row": "ה+ו"
      },
      {
        "group": "ה",
        "time": "8.00-9.30",
        "subject": "שפה עם רינת",
        "row": "ה+ו"
      }
    ]
  },
  {
    "week": 3,
    "day_header": "יום שלישי 14.7",
    "day_name": "יום שלישי",
    "date": "14.7",
    "file": "_תכנון שבועי 3 בית ספר של החופש הגדול כיתות ד-ו.docx",
    "sessions": [
      {
        "group": "ד (קב' 1)",
        "time": "10.00-11.30",
        "subject": "שפה עם שחר",
        "row": "ד"
      },
      {
        "group": "ד (קב' 1)",
        "time": "12.00-13.00",
        "subject": "העשרה באומנות עם מירב",
        "row": "ד"
      },
      {
        "group": "ד (קב' 2)",
        "time": "8.00-9.30",
        "subject": "שפה עם שחר",
        "row": "ד"
      },
      {
        "group": "ד (קב' 2)",
        "time": "10.00-11.30",
        "subject": "העשרה באומנות עם מירב",
        "row": "ד"
      },
      {
        "group": "ד (קב' 3)",
        "time": "8.00-9.30",
        "subject": "שפה עם מיכל ש.",
        "row": "ד"
      },
      {
        "group": "ה+ו",
        "time": "8.00-9.30",
        "subject": "העשרה באומנות עם מירב צ.",
        "row": "ה+ו"
      },
      {
        "group": "ה",
        "time": "9.30-11.00",
        "subject": "שפה עם רינת",
        "row": "ה+ו"
      },
      {
        "group": "ו",
        "time": "11.00-12.00",
        "subject": "שפה עם רינת",
        "row": "ה+ו"
      }
    ]
  },
  {
    "week": 3,
    "day_header": "יום רביעי 15.7",
    "day_name": "יום רביעי",
    "date": "15.7",
    "file": "_תכנון שבועי 3 בית ספר של החופש הגדול כיתות ד-ו.docx",
    "sessions": [
      {
        "group": "ד (קב' 1)",
        "time": "10.00-11.30",
        "subject": "העשרה באומנות עם מירב",
        "row": "ד"
      },
      {
        "group": "ד (קב' 2)",
        "time": "10.00-11.30",
        "subject": "שפה עם שחר",
        "row": "ד"
      },
      {
        "group": "ד (קב' 2)",
        "time": "12.00-13.00",
        "subject": "העשרה באומנות עם מירב",
        "row": "ד"
      },
      {
        "group": "ד (קב' 3)",
        "time": "8.00-9.30",
        "subject": "העשרה באומנות עם מירב",
        "row": "ד"
      },
      {
        "group": "ה",
        "time": "10.00-11.30",
        "subject": "שפה עם רינת",
        "row": "ה+ו"
      },
      {
        "group": "ו",
        "time": "8.00-9.30",
        "subject": "שפה עם רינת",
        "row": "ה+ו"
      }
    ]
  },
  {
    "week": 3,
    "day_header": "יום חמישי 16.7",
    "day_name": "יום חמישי",
    "date": "16.7",
    "file": "_תכנון שבועי 3 בית ספר של החופש הגדול כיתות ד-ו.docx",
    "sessions": [
      {
        "group": "ד (קב' 1)",
        "time": "12.00-13.00",
        "subject": "שפה עם שחר",
        "row": "ד"
      },
      {
        "group": "ד (קב' 2)",
        "time": "8.00-9.30",
        "subject": "שפה עם שחר",
        "row": "ד"
      },
      {
        "group": "ד (קב' 3)",
        "time": "12.00-13.00",
        "subject": "שפה עם שחר",
        "row": "ד"
      }
    ]
  },
  {
    "week": 4,
    "day_header": "יום ראשון 19.7",
    "day_name": "יום ראשון",
    "date": "19.7",
    "file": "_תכנון שבועי 4 בית ספר של החופש הגדול כיתות ד-ו.docx",
    "sessions": [
      {
        "group": "ד (קב' 1)",
        "time": "8.00-9.30",
        "subject": "אנגלית עם מיכל",
        "row": "ד"
      },
      {
        "group": "ד (קב' 1)",
        "time": "10.00-11.30",
        "subject": "שפה עם שחר",
        "row": "ד"
      },
      {
        "group": "ד (קב' 2)",
        "time": "8.00-9.30",
        "subject": "שפה עם שחר",
        "row": "ד"
      },
      {
        "group": "ד (קב' 2)",
        "time": "10.00-11.30",
        "subject": "אנגלית עם מיכל",
        "row": "ד"
      },
      {
        "group": "ד (קב' 3)",
        "time": "8.00-9.30",
        "subject": "שפה עם מיכל ש.",
        "row": "ד"
      },
      {
        "group": "ה",
        "time": "8.00-9.30",
        "subject": "שפה עם רינת",
        "row": "ה+ו"
      },
      {
        "group": "ו",
        "time": "10.00-11.30",
        "subject": "שפה עם רינת",
        "row": "ה+ו"
      },
      {
        "group": "ו",
        "time": "12.00-13.00",
        "subject": "אנגלית עם מיכל",
        "row": "ה+ו"
      }
    ]
  },
  {
    "week": 4,
    "day_header": "יום שני 20.7",
    "day_name": "יום שני",
    "date": "20.7",
    "file": "_תכנון שבועי 4 בית ספר של החופש הגדול כיתות ד-ו.docx",
    "sessions": [
      {
        "group": "ד (קב' 1)",
        "time": "10.00-11.30",
        "subject": "שפה עם שחר",
        "row": "ד"
      },
      {
        "group": "ד (קב' 1)",
        "time": "12.00-13.00",
        "subject": "אנגלית עם מיכל",
        "row": "ד"
      },
      {
        "group": "ד (קב' 2)",
        "time": "8.00-9.30",
        "subject": "שפה עם שחר",
        "row": "ד"
      },
      {
        "group": "ד (קב' 2)",
        "time": "10.00-11.00",
        "subject": "אנגלית עם מיכל",
        "row": "ד"
      },
      {
        "group": "ד (קב' 3)",
        "time": "11.00-12.00",
        "subject": "שפה עם שחר",
        "row": "ד"
      },
      {
        "group": "ה (ה' 1)",
        "time": "8.00-9.30",
        "subject": "אנגלית עם מיכל",
        "row": "ה+ו"
      },
      {
        "group": "ה",
        "time": "10.00-11.30",
        "subject": "שפה עם רינת",
        "row": "ה+ו"
      }
    ]
  },
  {
    "week": 4,
    "day_header": "יום שלישי 21.7",
    "day_name": "יום שלישי",
    "date": "21.7",
    "file": "_תכנון שבועי 4 בית ספר של החופש הגדול כיתות ד-ו.docx",
    "sessions": [
      {
        "group": "ד (קב' 1)",
        "time": "8.00-9.30",
        "subject": "אנגלית עם מיכל",
        "row": "ד"
      },
      {
        "group": "ד (קב' 1)",
        "time": "10.00-11.30",
        "subject": "שפה עם שחר",
        "row": "ד"
      },
      {
        "group": "ד (קב' 2)",
        "time": "8.00-9.30",
        "subject": "שפה עם שחר",
        "row": "ד"
      },
      {
        "group": "ד (קב' 3)",
        "time": "12.00-13.00",
        "subject": "שפה עם שחר",
        "row": "ד"
      },
      {
        "group": "ה (ה' 1)",
        "time": "8.00-9.30",
        "subject": "אנגלית עם מיכל",
        "row": "ה+ו"
      },
      {
        "group": "ה",
        "time": "10.00-11.30",
        "subject": "שפה עם רינת",
        "row": "ה+ו"
      }
    ]
  },
  {
    "week": 4,
    "day_header": "יום רביעי 22.7",
    "day_name": "יום רביעי",
    "date": "22.7",
    "file": "_תכנון שבועי 4 בית ספר של החופש הגדול כיתות ד-ו.docx",
    "sessions": [
      {
        "group": "ד (קב' 1)",
        "time": "8.00-9.30",
        "subject": "שפה עם שחר",
        "row": "ד"
      },
      {
        "group": "ד (קב' 1)",
        "time": "10.00-11.30",
        "subject": "אנגלית עם מיכל",
        "row": "ד"
      },
      {
        "group": "ד (קב' 2)",
        "time": "12.00-13.00",
        "subject": "אנגלית עם מיכל",
        "row": "ד"
      },
      {
        "group": "ד (קב' 3)",
        "time": "8.00-9.30",
        "subject": "אנגלית עם מיכל",
        "row": "ד"
      },
      {
        "group": "ד (קב' 3)",
        "time": "10.00-11.30",
        "subject": "שפה עם שחר",
        "row": "ד"
      }
    ]
  },
  {
    "week": 4,
    "day_header": "יום חמישי 23.7",
    "day_name": "יום חמישי",
    "date": "23.7",
    "file": "_תכנון שבועי 4 בית ספר של החופש הגדול כיתות ד-ו.docx",
    "sessions": [
      {
        "group": "ד (קב' 1)",
        "time": "8.00-9.30",
        "subject": "שפה עם שחר",
        "row": "ד"
      },
      {
        "group": "ד (קב' 1)",
        "time": "10.00-11.30",
        "subject": "אנגלית עם מיכל",
        "row": "ד"
      },
      {
        "group": "ד (קב' 2)",
        "time": "8.00-9.30",
        "subject": "אנגלית עם מיכל",
        "row": "ד"
      },
      {
        "group": "ד (קב' 2)",
        "time": "10.00-11.30",
        "subject": "שפה עם שחר",
        "row": "ד"
      }
    ]
  },
  {
    "week": 5,
    "day_header": "יום ראשון 26.7",
    "day_name": "יום ראשון",
    "date": "26.7",
    "file": "_ תכנון שבועי 5 בית ספר של החופש הגדול כיתות ד-ו.docx",
    "sessions": [
      {
        "group": "ד (קב' 1)",
        "time": "8.00-9.30",
        "subject": "שפה עם מיכל ש.",
        "row": "ד"
      },
      {
        "group": "ד (קב' 2)",
        "time": "10.00-11.30",
        "subject": "שפה עם מיכל ש.",
        "row": "ד"
      },
      {
        "group": "ד (קב' 3)",
        "time": "12.00-13.00",
        "subject": "שפה עם מיכל ש.",
        "row": "ד"
      },
      {
        "group": "ה (ה'1)",
        "time": "8.00-9.30",
        "subject": "אנגלית עם מיכל",
        "row": "ה+ו"
      },
      {
        "group": "ה (ה'2)",
        "time": "10.00-11.30",
        "subject": "אנגלית עם מיכל",
        "row": "ה+ו"
      },
      {
        "group": "ו",
        "time": "12.00-13.00",
        "subject": "אנגלית עם מיכל",
        "row": "ה+ו"
      }
    ]
  },
  {
    "week": 5,
    "day_header": "יום שני 27.7",
    "day_name": "יום שני",
    "date": "27.7",
    "file": "_ תכנון שבועי 5 בית ספר של החופש הגדול כיתות ד-ו.docx",
    "sessions": [
      {
        "group": "ד (קב' 1)",
        "time": "8.00-9.30",
        "subject": "אנגלית עם מיכל",
        "row": "ד"
      },
      {
        "group": "ד (קב' 1)",
        "time": "10.00-11.30",
        "subject": "שפה עם שחר",
        "row": "ד"
      },
      {
        "group": "ד (קב' 2)",
        "time": "8.00-9.30",
        "subject": "שפה עם שחר",
        "row": "ד"
      },
      {
        "group": "ד (קב' 2)",
        "time": "10.00-11.30",
        "subject": "אנגלית עם מיכל",
        "row": "ד"
      },
      {
        "group": "ד (קב' 3)",
        "time": "12.00-13.00",
        "subject": "אנגלית עם מיכל",
        "row": "ד"
      }
    ]
  },
  {
    "week": 5,
    "day_header": "יום שלישי 28.7",
    "day_name": "יום שלישי",
    "date": "28.7",
    "file": "_ תכנון שבועי 5 בית ספר של החופש הגדול כיתות ד-ו.docx",
    "sessions": [
      {
        "group": "ד (קב' 1)",
        "time": "8.00-9.30",
        "subject": "אנגלית עם מיכל",
        "row": "ד"
      },
      {
        "group": "ד (קב' 1)",
        "time": "10.00-11.30",
        "subject": "שפה עם מיכל ש.",
        "row": "ד"
      },
      {
        "group": "ד (קב' 2)",
        "time": "8.00-9.30",
        "subject": "שפה עם מיכל ש.",
        "row": "ד"
      },
      {
        "group": "ד (קב' 2)",
        "time": "10.00-11.30",
        "subject": "אנגלית עם מיכל",
        "row": "ד"
      }
    ]
  },
  {
    "week": 5,
    "day_header": "יום רביעי 29.7",
    "day_name": "יום רביעי",
    "date": "29.7",
    "file": "_ תכנון שבועי 5 בית ספר של החופש הגדול כיתות ד-ו.docx",
    "sessions": [
      {
        "group": "ד (קב' 1)",
        "time": "8.00-9.30",
        "subject": "שפה עם מיכל ש.",
        "row": "ד"
      },
      {
        "group": "ד (קב' 2)",
        "time": "12.00-13.00",
        "subject": "שפה עם מיכל ש.",
        "row": "ד"
      },
      {
        "group": "ד (קב' 3)",
        "time": "10.00-11.30",
        "subject": "שפה עם מיכל ש.",
        "row": "ד"
      },
      {
        "group": "ד (קב' 3)",
        "time": "12.00-13.00",
        "subject": "אנגלית עם מיכל",
        "row": "ד"
      },
      {
        "group": "ה (ה'1)",
        "time": "8.00-9.30",
        "subject": "אנגלית עם מיכל",
        "row": "ה+ו"
      },
      {
        "group": "ה (ה'2)",
        "time": "10.00-11.30",
        "subject": "אנגלית עם מיכל",
        "row": "ה+ו"
      }
    ]
  },
  {
    "week": 5,
    "day_header": "יום חמישי 30.7",
    "day_name": "יום חמישי",
    "date": "30.7",
    "file": "_ תכנון שבועי 5 בית ספר של החופש הגדול כיתות ד-ו.docx",
    "sessions": [
      {
        "group": "ד (קב' 1)",
        "time": "12.00-13.00",
        "subject": "אנגלית עם מיכל",
        "row": "ד"
      },
      {
        "group": "ד (קב' 2)",
        "time": "8.00-9.30",
        "subject": "אנגלית עם מיכל",
        "row": "ד"
      },
      {
        "group": "ד (קב' 2)",
        "time": "10.00-11.30",
        "subject": "שפה עם שחר",
        "row": "ד"
      },
      {
        "group": "ד (קב' 3)",
        "time": "8.00-9.30",
        "subject": "שפה עם שחר",
        "row": "ד"
      },
      {
        "group": "ד (קב' 3)",
        "time": "10.00-11.30",
        "subject": "אנגלית עם מיכל",
        "row": "ד"
      }
    ]
  }
]'''

# 2. מאגר שיבוץ התלמידים והקבוצות (הורד מהקבצים)
STUDENTS_JSON = '''{
  "אורין סירי": {
    "grade": "ד",
    "subjects": {
      "מתמטיקה": "קבוצה 1",
      "אנגלית": "קבוצה 1",
      "אמנות-העשרה": "קבוצה 2"
    }
  },
  "אור עמירה": {
    "grade": "ד",
    "subjects": {
      "מתמטיקה": "קבוצה 2",
      "אנגלית": "קבוצה 2",
      "שפה": "קבוצה 2",
      "אמנות-העשרה": "קבוצה 1"
    }
  },
  "איתן עטיה": {
    "grade": "ד",
    "subjects": {
      "מתמטיקה": "קבוצה 3"
    }
  },
  "ליאור מינץ": {
    "grade": "ד",
    "subjects": {
      "מתמטיקה": "קבוצה 1",
      "אנגלית": "קבוצה 1",
      "שפה": "קבוצה 1"
    }
  },
  "דריה קיש": {
    "grade": "ד",
    "subjects": {
      "מתמטיקה": "קבוצה 2"
    }
  },
  "מיקה קוט": {
    "grade": "ד",
    "subjects": {
      "מתמטיקה": "קבוצה 3",
      "אמנות-העשרה": "קבוצה 1"
    }
  },
  "לורן קובי": {
    "grade": "ד",
    "subjects": {
      "מתמטיקה": "קבוצה 1",
      "אנגלית": "קבוצה 1",
      "שפה": "קבוצה 1"
    }
  },
  "רומי דרור": {
    "grade": "ד",
    "subjects": {
      "מתמטיקה": "קבוצה 2"
    }
  },
  "אורי אפרגן": {
    "grade": "ד",
    "subjects": {
      "מתמטיקה": "קבוצה 3"
    }
  },
  "עומר מג'ר": {
    "grade": "ד",
    "subjects": {
      "מתמטיקה": "קבוצה 1",
      "אנגלית": "קבוצה 1",
      "שפה": "קבוצה 1",
      "אמנות-העשרה": "קבוצה 2"
    }
  },
  "ליבי נרינסקי": {
    "grade": "ד",
    "subjects": {
      "מתמטיקה": "קבוצה 2",
      "שפה": "קבוצה 2",
      "אמנות-העשרה": "קבוצה 1"
    }
  },
  "עופרי דרור": {
    "grade": "ד",
    "subjects": {
      "מתמטיקה": "קבוצה 3",
      "אנגלית": "קבוצה 3",
      "שפה": "קבוצה 2"
    }
  },
  "רועי קינן": {
    "grade": "ד",
    "subjects": {
      "מתמטיקה": "קבוצה 1",
      "שפה": "קבוצה 1"
    }
  },
  "נויה הדר": {
    "grade": "ד",
    "subjects": {
      "מתמטיקה": "קבוצה 2",
      "אנגלית": "קבוצה 2"
    }
  },
  "נדב האוסמן": {
    "grade": "ד",
    "subjects": {
      "מתמטיקה": "קבוצה 3",
      "שפה": "קבוצה 2"
    }
  },
  "יובל זהבי": {
    "grade": "ד",
    "subjects": {
      "מתמטיקה": "קבוצה 1",
      "אנגלית": "קבוצה 1",
      "שפה": "קבוצה 1"
    }
  },
  "יהונתן הראל": {
    "grade": "ד",
    "subjects": {
      "מתמטיקה": "קבוצה 3",
      "אנגלית": "קבוצה 3",
      "שפה": "קבוצה 2",
      "אמנות-העשרה": "קבוצה 1"
    }
  },
  "נוב מושקט": {
    "grade": "ד",
    "subjects": {
      "מתמטיקה": "קבוצה 3",
      "אנגלית": "קבוצה 3",
      "שפה": "קבוצה 2"
    }
  },
  "ליה שולוב": {
    "grade": "ד",
    "subjects": {
      "מתמטיקה": "קבוצה 1",
      "שפה": "קבוצה 1",
      "אמנות-העשרה": "קבוצה 2"
    }
  },
  "יובל פרבר": {
    "grade": "ד",
    "subjects": {
      "מתמטיקה": "קבוצה 2",
      "אנגלית": "קבוצה 2"
    }
  },
  "דן שבת": {
    "grade": "ד",
    "subjects": {
      "מתמטיקה": "קבוצה 3",
      "אנגלית": "קבוצה 2",
      "שפה": "קבוצה 1",
      "אמנות-העשרה": "קבוצה 2"
    }
  },
  "עופרי בר שלום": {
    "grade": "ד",
    "subjects": {
      "מתמטיקה": "קבוצה 1"
    }
  },
  "איתן סייקין": {
    "grade": "ד",
    "subjects": {
      "מתמטיקה": "קבוצה 2",
      "אנגלית": "קבוצה 2",
      "שפה": "קבוצה 2",
      "אמנות-העשרה": "קבוצה 1"
    }
  },
  "עמית הלפרין": {
    "grade": "ד",
    "subjects": {
      "מתמטיקה": "קבוצה 3",
      "אנגלית": "קבוצה 3",
      "שפה": "קבוצה 2",
      "אמנות-העשרה": "קבוצה 1"
    }
  },
  "אלמה מור": {
    "grade": "ד",
    "subjects": {
      "מתמטיקה": "קבוצה 1"
    }
  },
  "נבו דגן": {
    "grade": "ד",
    "subjects": {
      "מתמטיקה": "קבוצה 2",
      "אנגלית": "קבוצה 2",
      "אמנות-העשרה": "קבוצה 2"
    }
  },
  "נדב ירון": {
    "grade": "ד",
    "subjects": {
      "מתמטיקה": "קבוצה 3",
      "אנגלית": "קבוצה 3",
      "שפה": "קבוצה 2",
      "אמנות-העשרה": "קבוצה 1"
    }
  },
  "מיקה תשובה": {
    "grade": "ד",
    "subjects": {
      "מתמטיקה": "קבוצה 1",
      "שפה": "קבוצה 1"
    }
  },
  "ירדן שגב": {
    "grade": "ד",
    "subjects": {
      "מתמטיקה": "קבוצה 2"
    }
  },
  "טל זגורי": {
    "grade": "ד",
    "subjects": {
      "מתמטיקה": "קבוצה 3",
      "אנגלית": "קבוצה 3",
      "שפה": "קבוצה 2",
      "אמנות-העשרה": "קבוצה 1"
    }
  },
  "ליה בלייר": {
    "grade": "ד",
    "subjects": {
      "מתמטיקה": "קבוצה 1",
      "אמנות-העשרה": "קבוצה 2"
    }
  },
  "ירום עוז": {
    "grade": "ד",
    "subjects": {
      "מתמטיקה": "קבוצה 2",
      "אמנות-העשרה": "קבוצה 2"
    }
  },
  "נועה שילמן": {
    "grade": "ד",
    "subjects": {
      "מתמטיקה": "קבוצה 1",
      "אנגלית": "קבוצה 1",
      "אמנות-העשרה": "קבוצה 2"
    }
  },
  "לילי רייני": {
    "grade": "ד",
    "subjects": {
      "מתמטיקה": "קבוצה 3"
    }
  },
  "ליה רייני": {
    "grade": "ד",
    "subjects": {
      "מתמטיקה": "קבוצה 3"
    }
  },
  "סהר מצנר": {
    "grade": "ד",
    "subjects": {
      "אנגלית": "קבוצה 3",
      "אמנות-העשרה": "קבוצה 2"
    }
  },
  "אורי איפרגן": {
    "grade": "ד",
    "subjects": {
      "אנגלית": "קבוצה 3",
      "אמנות-העשרה": "קבוצה 2"
    }
  },
  "נבו מדג'ר": {
    "grade": "ד",
    "subjects": {
      "אנגלית": "קבוצה 1"
    }
  },
  "עידו עוקב": {
    "grade": "ד",
    "subjects": {
      "אנגלית": "קבוצה 3",
      "אמנות-העשרה": "קבוצה 1"
    }
  },
  "עלמה שמר": {
    "grade": "ד",
    "subjects": {
      "אנגלית": "קבוצה 1"
    }
  },
  "קרן מירב": {
    "grade": "ד",
    "subjects": {
      "אנגלית": "קבוצה 2",
      "אמנות-העשרה": "קבוצה 1"
    }
  },
  "מיקה תבל": {
    "grade": "ד",
    "subjects": {
      "אנגלית": "קבוצה 2",
      "שפה": "קבוצה 1"
    }
  },
  "שני המר": {
    "grade": "ד",
    "subjects": {
      "אנגלית": "קבוצה 3"
    }
  },
  "גרינר לביא": {
    "grade": "ד",
    "subjects": {
      "שפה": "קבוצה 1"
    }
  },
  "עמנואל ארזואן": {
    "grade": "ד",
    "subjects": {
      "אמנות-העשרה": "קבוצה 2"
    }
  },
  "שחר כץ": {
    "grade": "ד",
    "subjects": {
      "אמנות-העשרה": "קבוצה 2"
    }
  },
  "שרי בן חמו": {
    "grade": "ד",
    "subjects": {
      "אמנות-העשרה": "קבוצה 1"
    }
  },
  "שחר דרור": {
    "grade": "ה",
    "subjects": {
      "מתמטיקה": "רשומה",
      "שפה": "רשומה",
      "אנגלית": "קבוצה 1",
      "אמנות-העשרה": "רשומה"
    }
  },
  "עילאי מסיקה": {
    "grade": "ה",
    "subjects": {
      "מתמטיקה": "רשומה",
      "שפה": "רשומה",
      "אנגלית": "קבוצה 2"
    }
  },
  "ליאם בן אהרון": {
    "grade": "ה",
    "subjects": {
      "מתמטיקה": "רשומה"
    }
  },
  "אדם אלפרון": {
    "grade": "ה",
    "subjects": {
      "מתמטיקה": "רשומה",
      "שפה": "רשומה",
      "אנגלית": "קבוצה 1",
      "אמנות-העשרה": "רשומה"
    }
  },
  "אלון שחורי": {
    "grade": "ה",
    "subjects": {
      "מתמטיקה": "רשומה",
      "שפה": "רשומה",
      "אנגלית": "קבוצה 2"
    }
  },
  "שחר רובינשטיין": {
    "grade": "ה",
    "subjects": {
      "מתמטיקה": "רשומה",
      "שפה": "רשומה",
      "אנגלית": "קבוצה 1"
    }
  },
  "ארי ברוקס": {
    "grade": "ה",
    "subjects": {
      "מתמטיקה": "רשומה",
      "שפה": "רשומה",
      "אנגלית": "קבוצה 1"
    }
  },
  "אסיף רוזמן": {
    "grade": "ה",
    "subjects": {
      "מתמטיקה": "רשומה"
    }
  },
  "עילאי סיגל": {
    "grade": "ה",
    "subjects": {
      "מתמטיקה": "רשומה",
      "שפה": "רשומה",
      "אנגלית": "קבוצה 2",
      "אמנות-העשרה": "רשומה"
    }
  },
  "שלו עבדת": {
    "grade": "ה",
    "subjects": {
      "מתמטיקה": "רשומה",
      "אנגלית": "קבוצה 1"
    }
  },
  "שקד שגיא": {
    "grade": "ה",
    "subjects": {
      "שפה": "רשומה"
    }
  },
  "אסיף רוזן": {
    "grade": "ה",
    "subjects": {
      "שפה": "רשומה",
      "אנגלית": "קבוצה 2"
    }
  },
  "יהונתן במני": {
    "grade": "ה",
    "subjects": {
      "אנגלית": "קבוצה 1"
    }
  },
  "קארה אפשטיין": {
    "grade": "ה",
    "subjects": {
      "אנגלית": "קבוצה 2"
    }
  },
  "יובל מלכה": {
    "grade": "ה",
    "subjects": {
      "אנגלית": "קבוצה 2"
    }
  },
  "מיכאל ארזואן": {
    "grade": "ה",
    "subjects": {
      "אנגלית": "קבוצה 2"
    }
  },
  "מיאל צמח": {
    "grade": "ה",
    "subjects": {
      "אנגלית": "קבוצה 2"
    }
  },
  "אריאל קורן": {
    "grade": "ה",
    "subjects": {
      "אנגלית": "קבוצה 1"
    }
  },
  "דני יפרח": {
    "grade": "ה",
    "subjects": {
      "אנגלית": "קבוצה 1"
    }
  },
  "עמית חוליו": {
    "grade": "ה",
    "subjects": {
      "אנגלית": "קבוצה 1"
    }
  },
  "עילי מזרחי": {
    "grade": "ה",
    "subjects": {
      "אנגלית": "קבוצה 2"
    }
  },
  "שקד שגיא שחר רובינשטיין": {
    "grade": "ה+ו",
    "subjects": {
      "אמנות-העשרה": "רשומה"
    }
  },
  "סול מצנר": {
    "grade": "ה+ו",
    "subjects": {
      "אמנות-העשרה": "רשומה",
      "מתמטיקה": "רשומה"
    }
  },
  "אופק רובינשטיין": {
    "grade": "ה+ו",
    "subjects": {
      "אמנות-העשרה": "רשומה",
      "מתמטיקה": "רשומה",
      "אנגלית": "רשומה",
      "שפה": "רשומה"
    }
  },
  "עומר דורון": {
    "grade": "ה+ו",
    "subjects": {
      "אמנות-העשרה": "רשומה",
      "מתמטיקה": "רשומה",
      "אנגלית": "רשומה",
      "שפה": "רשומה"
    }
  },
  "נעמי פרץ": {
    "grade": "ו",
    "subjects": {
      "מתמטיקה": "רשומה"
    }
  },
  "רביד ישראלי": {
    "grade": "ו",
    "subjects": {
      "מתמטיקה": "רשומה"
    }
  },
  "נאיה קמחי": {
    "grade": "ו",
    "subjects": {
      "מתמטיקה": "רשומה",
      "אנגלית": "רשומה"
    }
  },
  "אריאל פרבר": {
    "grade": "ו",
    "subjects": {
      "מתמטיקה": "רשומה",
      "אנגלית": "רשומה"
    }
  },
  "תמר ביטון": {
    "grade": "ו",
    "subjects": {
      "מתמטיקה": "רשומה",
      "אנגלית": "רשומה",
      "שפה": "רשומה"
    }
  },
  "אלון קלאורה": {
    "grade": "ו",
    "subjects": {
      "אנגלית": "רשומה"
    }
  },
  "אביב קלאורה": {
    "grade": "ו",
    "subjects": {
      "אנגלית": "רשומה"
    }
  },
  "נבו ברין": {
    "grade": "ו",
    "subjects": {
      "אנגלית": "רשומה"
    }
  },
  "יונתן מרום": {
    "grade": "ו",
    "subjects": {
      "אנגלית": "רשומה"
    }
  },
  "אגם ארזי": {
    "grade": "ו",
    "subjects": {
      "אנגלית": "רשומה"
    }
  }
}'''

days = json.loads(SESSIONS_JSON)
students = json.loads(STUDENTS_JSON)

def disp(text):
    if not REVERSE_HEBREW:
        return text
    try:
        from bidi.algorithm import get_display
        return get_display(text)
    except ImportError:
        import subprocess
        import sys
        try:
            # Install python-bidi silently if missing and REVERSE_HEBREW is True
            subprocess.check_call([sys.executable, "-m", "pip", "install", "python-bidi"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
            from bidi.algorithm import get_display
            return get_display(text)
        except Exception:
            # Simple fallback letter reversal if pip is offline/fails
            return text[::-1]

def normalize_time(time_str):
    if not time_str:
        return ""
    m = re.match(r'(\d+)[\.:](\d+)\s*-\s*(\d+)[\.:](\d+)', time_str)
    if m:
        h1, m1, h2, m2 = m.groups()
        return f"{int(h1):02d}:{int(m1):02d}-{int(h2):02d}:{int(m2):02d}"
    return time_str

def get_subject_type(subj_text):
    s = subj_text.lower()
    if 'שפה' in s:
        return 'שפה'
    elif 'מתמטיקה' in s:
        return 'מתמטיקה'
    elif 'אנגלית' in s:
        return 'אנגלית'
    elif 'אומנות' in s or 'אמנות' in s or 'העשרה' in s:
        return 'אמנות-העשרה'
    return 'unknown'

def check_student_attendance(student_name, session):
    if student_name not in students:
        return False
        
    s_info = students[student_name]
    s_grade = s_info['grade']
    s_subjects = s_info['subjects']
    
    group = session['group']
    row_type = session['row']
    subj_text = session['subject']
    subj_type = get_subject_type(subj_text)
    
    # Extract group number for ד or ה
    group_num = None
    if group:
        m = re.search(r'\d+', group)
        if m:
            group_num = int(m.group(0))
            
    # Class Grade ד
    if row_type == 'ד' or (group and 'ד' in group):
        if s_grade == 'ד':
            if subj_type in s_subjects:
                s_group = s_subjects[subj_type] # e.g. "קבוצה 3"
                s_group_num_m = re.search(r'\d+', s_group)
                if s_group_num_m:
                    s_group_num = int(s_group_num_m.group(0))
                    if s_group_num == group_num:
                        return True
        return False
        
    # Class Grade ה+ו or ו
    if row_type == 'ה+ו' or (group and ('ו' in group or 'ה+ו' in group)):
        is_grade_f_or_combined = False
        if group in ['ו', 'ה+ו']:
            is_grade_f_or_combined = True
        elif 'ו' in group and 'ה' not in group:
            is_grade_f_or_combined = True
        elif 'ה+ו' in group:
            is_grade_f_or_combined = True
            
        if is_grade_f_or_combined:
            if s_grade == 'ו':
                if subj_type in s_subjects:
                    return True
            elif s_grade == 'ה+ו':
                if subj_type in s_subjects:
                    return True
        return False
        
    # Class Grade ה
    if group and 'ה' in group and 'ו' not in group:
        if s_grade == 'ה':
            if subj_type in s_subjects:
                s_group = s_subjects[subj_type] # e.g. "קבוצה 1"
                if group_num:
                    s_group_num_m = re.search(r'\d+', s_group)
                    if s_group_num_m:
                        s_group_num = int(s_group_num_m.group(0))
                        if s_group_num == group_num:
                            return True
                else:
                    return True
        return False
        
    return False

def query_schedule(query):
    query = query.strip()
    if not query:
        return
        
    # 1. Search for student name (case/whitespace insensitive)
    student_found = None
    for s_name in students.keys():
        if s_name.lower().replace(" ", "") == query.lower().replace(" ", ""):
            student_found = s_name
            break
            
    if student_found:
        print(disp("="*60))
        print(disp(f" נמצא/ה תלמיד/ה: {student_found} (כיתה {students[student_found]['grade']}')"))
        print(disp(" קבוצות שיבוץ:"))
        for subj, grp in students[student_found]['subjects'].items():
            print(disp(f"  • {subj}: {grp}"))
        print(disp("="*60))
        print(disp("\n📅 לוח שעות אישי לחודש יולי:"))
        
        has_classes = False
        for w in range(1, 6):
            print(disp(f"\n--- שבוע {w} ---"))
            week_days = [d for d in days if d['week'] == w]
            day_to_order = {"יום ראשון": 0, "יום שני": 1, "יום שלישי": 2, "יום רביעי": 3, "יום חמישי": 4}
            week_days.sort(key=lambda x: day_to_order.get(x['day_name'], 5))
            
            for day in week_days:
                day_sessions = []
                for s in day['sessions']:
                    if check_student_attendance(student_found, s):
                        day_sessions.append(s)
                        
                if day_sessions:
                    has_classes = True
                    print(disp(f"  * {day['day_name']} ({day['date']}):"))
                    def get_time_key(s_dict):
                        t = normalize_time(s_dict['time'])
                        m = re.match(r'(\d+):(\d+)', t)
                        return (int(m.group(1)), int(m.group(2))) if m else (24, 0)
                    day_sessions.sort(key=get_time_key)
                    
                    for s in day_sessions:
                        print(disp(f"    - {normalize_time(s['time'])} | {s['group']} | {s['subject']}"))
                        
        if not has_classes:
            print(disp("  אין שיעורים מתוכננים בחודש יולי."))
        return

    # 2. Search for group (e.g. "ד קבוצה 1", "קב' 3", "כיתות ו")
    query_clean = query.lower()
    
    # Try matching specific grade + group
    match_d_g = re.search(r"([דהו])\s*(?:קבוצה|קב|קב')\s*(\d+)", query_clean)
    query_grade = None
    query_group_num = None
    
    if match_d_g:
        query_grade = match_d_g.group(1)
        query_group_num = int(match_d_g.group(2))
    else:
        m_grade = re.match(r'^([דהו])$', query_clean)
        if m_grade:
            query_grade = m_grade.group(1)
            
    if query_grade:
        print(disp("="*60))
        group_desc = f"כיתה {query_grade}"
        if query_group_num:
            group_desc += f" (קבוצה {query_group_num})"
        print(disp(f" סינון שיעורים עבור: {group_desc}"))
        print(disp("="*60))
        
        has_classes = False
        for w in range(1, 6):
            print(disp(f"\n--- שבוע {w} ---"))
            week_days = [d for d in days if d['week'] == w]
            day_to_order = {"יום ראשון": 0, "יום שני": 1, "יום שלישי": 2, "יום רביעי": 3, "יום חמישי": 4}
            week_days.sort(key=lambda x: day_to_order.get(x['day_name'], 5))
            
            for day in week_days:
                day_sessions = []
                for s in day['sessions']:
                    group = s['group'] or s['row']
                    grade_match = False
                    if query_grade in group:
                        grade_match = True
                    elif query_grade == 'ו' and 'ה+ו' in group:
                        grade_match = True
                    elif query_grade == 'ה' and 'ה+ו' in group:
                        grade_match = True
                        
                    if grade_match:
                        if query_group_num:
                            m_num = re.search(r'\d+', group)
                            if m_num and int(m_num.group(0)) == query_group_num:
                                day_sessions.append(s)
                        else:
                            day_sessions.append(s)
                            
                if day_sessions:
                    has_classes = True
                    print(disp(f"  * {day['day_name']} ({day['date']}):"))
                    def get_time_key(s_dict):
                        t = normalize_time(s_dict['time'])
                        m = re.match(r'(\d+):(\d+)', t)
                        return (int(m.group(1)), int(m.group(2))) if m else (24, 0)
                    day_sessions.sort(key=get_time_key)
                    for s in day_sessions:
                        print(disp(f"    - {normalize_time(s['time'])} | {s['group']} | {s['subject']}"))
                        
        if not has_classes:
            print(disp("  אין שיעורים מתוכננים."))
        return

    # 3. Suggest names if name was misspelled
    close_matches = difflib.get_close_matches(query, students.keys(), n=3, cutoff=0.5)
    print(disp("="*60))
    print(disp(f" הזינו: '{query}' - החיפוש לא הניב תוצאות."))
    if close_matches:
        print(disp(" האם התכוונתם ל:"))
        for m in close_matches:
            print(disp(f"  • {m}"))
    else:
        print(disp(" הנחיות חיפוש:"))
        print(disp("  - לחיפוש תלמיד: הזינו שם מלא (למשל: סהר מצנר)"))
        print(disp("  - לחיפוש קבוצה: הזינו 'ד קבוצה 1', 'ה קבוצה 2', 'ו' וכד'"))
    print(disp("="*60))

# Interactive loop
print(disp("=============================================================="))
print(disp("     ברוכים הבאים ללוח השיעורים האינטראקטיבי - יולי 2026"))
print(disp("=============================================================="))
print(disp("הקלידו שם של תלמיד/ה או שם קבוצה כדי לקבל לוח שעות מותאם אישית."))
print(disp("לסיום החיפוש, הקלידו 'יציאה' או 'exit'.\n"))

while True:
    q = input(disp("הזן שם תלמיד/ה או קבוצה (או 'יציאה' לסיום): "))
    if q.strip().lower() in ['יציאה', 'exit', 'quit', 'סגור']:
        print(disp("להתראות!"))
        break
    query_schedule(q)
    print("\n" + disp("="*80) + "\n")
