using System.Collections.Generic;
using TMPro;
using UnityEngine;
using UnityEngine.UI;

namespace Utility
{
    public class UIResizer : MonoBehaviour
    {
        public List<TextMeshProUGUI> texts;
        public List<Button> btns;
        public List<TMP_InputField> fields;

        public Vector2 TMPsize;
        public Vector2 TMPBTNsize;
        public Vector2 TMPInputFieldsize;

        [ContextMenu("delete references")]
        public void delete()
        {
            texts.Clear();
            btns.Clear();
            fields.Clear();
        }

        [ContextMenu("Resize TMP")]
        public void Resize()
        {
            foreach (var text in texts)
            {
                text.transform.localScale = Vector3.one;
                var rectTransform = text.GetComponent<RectTransform>();
                if (rectTransform != null)
                    // Set the size of the RectTransform
                    rectTransform.sizeDelta = TMPsize;
            }


            foreach (var btn in btns)
            {
                btn.transform.localScale = Vector3.one;
                var rectTransform = btn.GetComponent<RectTransform>();
                if (rectTransform != null)
                    // Set the size of the RectTransform
                    rectTransform.sizeDelta = TMPBTNsize;
            }


            foreach (var field in fields)
            {
                field.transform.localScale = Vector3.one;
                var rectTransform = field.GetComponent<RectTransform>();
                if (rectTransform != null)
                    // Set the size of the RectTransform
                    rectTransform.sizeDelta = TMPInputFieldsize;
            }
        }
    }
}