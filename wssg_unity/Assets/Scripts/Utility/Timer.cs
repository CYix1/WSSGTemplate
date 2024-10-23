using UnityEngine;
using UnityEngine.Events;

namespace Utility
{
    public class Timer : MonoBehaviour
    {
        public float maxTime = 10f;
        public UnityEvent timerFinished;
        public bool loop;
        public bool stopped;
        public bool showPrint;
        private float currentTime;

        private void Start()
        {
            if (timerFinished == null)
                timerFinished = new UnityEvent();
        }

        private void Update()
        {
            if (stopped)
                return;
            currentTime += Time.deltaTime;
            if (!(currentTime > maxTime)) return;

            timerFinished.Invoke();
            if (showPrint)
                Debug.Log("Timer Invoked");
            if (loop)
                currentTime = 0;
            else
                stopped = true;
        }
    }
}