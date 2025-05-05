using System;

namespace MyDotNetApi.Tools
{
    [AttributeUsage(AttributeTargets.Class)]
    public class FunctionToolAttribute : Attribute
    {
        public string Name { get; }
        public string Description { get; }

        public FunctionToolAttribute(string name, string description)
        {
            Name = name;
            Description = description;
        }
    }
}
