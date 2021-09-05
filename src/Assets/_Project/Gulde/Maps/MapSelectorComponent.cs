using MonoLogger.Runtime;
using Sirenix.OdinInspector;
using Sirenix.Serialization;
using UnityEngine;

namespace Gulde.Maps
{
    public class MapSelectorComponent : SerializedMonoBehaviour
    {
        [OdinSerialize]
        [InlineButton("Select")]
        public MapComponent SelectedMap { get; set; }

        void Awake()
        {
            Locator.MapSelector = this;
        }

        void Select()
        {
            if (!SelectedMap) return;

            foreach (var map in MapRegistry.Maps)
            {
                map.SetVisible(map == SelectedMap);
                this.Log($"Set map {map.name} to {(map == SelectedMap ? "visible" : "invisible")}");
            }
        }
    }
}